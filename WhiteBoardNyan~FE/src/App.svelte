<script>
  import Icon from "@iconify/svelte";
  import { onMount } from "svelte";

  let RESOURCE_ROOT = "/static/frontend/";

  let whiteboardlogo = RESOURCE_ROOT + "image/WhiteBoardIcon-2.png";

  let canvas, ctx;
  let previousX = Infinity;
  let previousY = Infinity;
  let colorPaletteValue;
  let colorHue = "#000000";

  let pencilIcon, eraserIcon, selectColorIcon, nextIcon, previousIcon;
  let toolSelected = "0";

  window.addEventListener("resize", () => {
    const temp = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const { x, width, y, height } = canvas.getBoundingClientRect();
    canvas.width = width;
    canvas.height = height;

    ctx = canvas.getContext("2d");
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    ctx.lineWidth = 10;
    ctx.putImageData(temp, 0, 0);
  });

  // WebSocket config
  let userID = generate_user_id();
  
  let hostname = window.location.host;
  let path = window.location.pathname;
  let roomCode = path.split("/");
  roomCode = roomCode[roomCode.length - 1];

  let connection = new WebSocket('ws://' + hostname + "/ws/whiteboard/" + roomCode + "/");

  connection.onopen = webSocketInit;
  connection.onclose = webSocketClose;
  connection.onmessage = messageHandler;

  if (connection.readyState == WebSocket.OPEN) {
    connection.onopen();
  }

  // Handling Key Press
  document.onkeyup = keyPressHandler;

  onMount(() => {
    initialize();

    return () => {
      // unMount
    };
  });

  function generate_user_id() {
    const hexChar = "0123456789abcdef";
    let result = "";

    for (let i = 0; i < 32; i++) {
        result += hexChar.charAt(Math.floor(Math.random() * hexChar.length));
    }

    return result;
  }

  function send(message) {
    connection.send(JSON.stringify(message));
  }

  function initialize() {
    const { x, width, y, height } = canvas.getBoundingClientRect();
    canvas.width = width;
    canvas.height = height;

    ctx = canvas.getContext("2d");
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    ctx.lineWidth = 10;

    colorPaletteValue = document.querySelector("#colorpicker");
    colorPaletteValue.addEventListener("change", updateColor, true);
  }

  function paint(e) {
    let clientX_msg;
    let clientY_msg;
    let offsetX_msg;
    let offsetY_msg;
    let colorHue_msg = colorHue;
    
    if (toolSelected == "1") {
      const { clientX, clientY, offsetX, offsetY } = e;
      ctx.strokeStyle = colorHue;
      ctx.beginPath();

      clientX_msg = clientX;
      clientY_msg = clientY;
      offsetX_msg = offsetX;
      offsetY_msg = offsetY;

      if (
        Math.abs(previousX - clientX) < 100 &&
        Math.abs(previousY - clientY) < 100
      ) {
        ctx.moveTo(previousX, previousY);
        clientX_msg = previousX;
        clientY_msg = previousY;
      }

      ctx.lineTo(offsetX, offsetY);
      ctx.stroke();
      previousX = offsetX;
      previousY = offsetY;
    } else if (toolSelected == "2") {
      const { clientX, clientY, offsetX, offsetY } = e;
      ctx.strokeStyle = "#ffffff";
      ctx.beginPath();

      clientX_msg = clientX;
      clientY_msg = clientY;
      offsetX_msg = offsetX;
      offsetY_msg = offsetY;

      if (
        Math.abs(previousX - clientX) < 100 &&
        Math.abs(previousY - clientY) < 100
      ) {
        ctx.moveTo(previousX, previousY);
        clientX_msg = previousX;
        clientY_msg = previousY;
      }

      ctx.lineTo(offsetX, offsetY);
      ctx.stroke();
      previousX = offsetX;
      previousY = offsetY;
    }

    send({
        event: "MESSAGE",
        data: "Drawing",
        userID: userID,
    });

    send({
      event: "DRAW",
      data: {
        action: toolSelected,
        clientX: clientX_msg,
        clientY: clientY_msg,
        offsetX: offsetX_msg,
        offsetY: offsetY_msg,
        colorHue: colorHue_msg,
        userID: userID,
      }
    });
  }

  function updateColor(event) {
    colorHue = event.target.value;
    console.log("update color selected");
    console.log(event.target.value);
    console.log(colorHue);
  }

  function onMouseMove(event) {
    paint(event);
  }

  function onMouseDown(event) {
    canvas.addEventListener("mousemove", onMouseMove);
    canvas.addEventListener("mouseup", onMouseUp);
  }

  function onMouseUp() {
    canvas.removeEventListener("mousemove", onMouseMove);
    canvas.removeEventListener("mouseup", onMouseUp);
    previousX = Infinity;
    previousY = Infinity;
  }

  function selectedTool() {
    pencilIcon.style.backgroundColor = "#ededed";
    eraserIcon.style.backgroundColor = "#ededed";
    selectColorIcon.style.backgroundColor = "#ededed";
    nextIcon.style.backgroundColor = "#ededed";
    previousIcon.style.backgroundColor = "#ededed";

    switch (toolSelected) {
      case "0": {
        break;
      }
      case "1": {
        pencilIcon.style.backgroundColor = "grey";
        break;
      }
      case "2": {
        eraserIcon.style.backgroundColor = "grey";
        break;
      }
      case "3": {
        selectColorIcon.style.backgroundColor = "grey";
        break;
      }
      case "4": {
        nextIcon.style.backgroundColor = "grey";
        break;
      }
      case "5": {
        previousIcon.style.backgroundColor = "grey";
        break;
      }
    }
  }

  // Web Socket functions
  function webSocketInit() {
    console.log("Connected to WebSocket");
  }

  function webSocketClose() {
    console.log("Closed WebSocket Connection");
  }

  function messageHandler(message) {
    console.log("Received message");
    console.log(message)
    let content = JSON.parse(message.data);
    let payload = content.payload;
    let data = payload.data;
    let senderID = data.userID;

    console.log("MY ID = " + userID);
    console.log(payload);

    if (senderID == userID) {
        return;
    }

    switch(payload.event) {
      case "MESSAGE":
        console.log(data);
        break;
      case "DRAW":
        console.log(data);
        drawFromMessage(data);
        break;
      case "ALERT":
        alert(data);
        break;
      default:
        break;
    }

    if (connection.readyState == WebSocket.OPEN) {
        connection.onopen();
    }
  }

  function drawFromMessage(messageData) {
    if (messageData.action == "1") {
      ctx.strokeStyle = messageData.colorHue;
      ctx.beginPath();

      ctx.moveTo(messageData.clientX, messageData.clientY);

      ctx.lineTo(messageData.offsetX, messageData.offsetY);
      ctx.stroke();
    }
    else if(messageData.action == "2"){
      ctx.strokeStyle = messageData.colorHue;
      ctx.beginPath();

      ctx.moveTo(messageData.clientX, messageData.clientY);

      ctx.lineTo(messageData.offsetX, messageData.offsetY);
      ctx.stroke();
      colorHue = "#ffffff";
    }
  }

  function keyPressHandler(e) {
    let key = e.key;

    if (key == "Escape") {
        toolSelected = "0";
        selectedTool();
    }
  }
</script>

<main>
  <div class="main-page">
    <div class="header">
      <div class="icon-name">
        <div class="icon">
          <img src={whiteboardlogo} alt="whiteboardlogo" />
        </div>
        <div class="app-title">Cooperative Whiteboard</div>
      </div>
      <div class="whiteboard-name">Whiteboard Title</div>
      <div class="user">
        <div class="user-icon">
          <!-- <img/> -->
        </div>
        <div class="user-name">UserTEMP</div>
        <div class="sign-out">Sign Out</div>
      </div>
    </div>

    <div class="center-page">
      <div class="tool-bar">
        <div
          class="tool-icon"
          bind:this={pencilIcon}
          on:click={() => (toolSelected = "1")}
          on:click={selectedTool}
        >
          <Icon
            icon="fluent-emoji-high-contrast:pencil"
            width="32"
            height="32"
          />
        </div>
        <div
          class="tool-icon"
          bind:this={eraserIcon}
          on:click={() => (toolSelected = "2")}
          on:click={selectedTool}
        >
          <Icon icon="icons8:eraser" width="44" height="44" />
        </div>
        <div
          class="tool-icon"
          bind:this={selectColorIcon}
          on:click={() => (toolSelected = "3")}
          on:click={selectedTool}
        >
          <input type="color" id="colorpicker" />
        </div>
        <div class="tool-icon"
          bind:this={nextIcon}
          on:click={()=> (toolSelected= "4")}
          on:click={selectedTool}
        >
          <Icon icon="fluent:next-20-filled" width="44" height="44"></Icon>
        </div>
        <div class="tool-icon">
          <form id="page-no-form" action="">
            <input type="text" id="currentPage">
          </form>
        </div>
        <div
          class="tool-icon"
          bind:this={previousIcon}
          on:click={() => (toolSelected = "5")}
          on:click={selectedTool}
          >
            <Icon icon="fluent:previous-48-filled" width="44" height="44"></Icon>
        </div>
      </div>
      <div class="canvas">
        <canvas
          id="my-canvas"
          bind:this={canvas}
          on:mousedown={onMouseDown}
          on:mouseup={onMouseUp}
        />
        <canvas
          id="canvas"
          style="background-color:#EEE;"
          width="500px"
          height="200px"
        />
        <script type="text/javascript">
          var canvas = document.getElementById("canvas");
          var ctx = canvas.getContext("2d");
          canvas.addEventListener(
            "mousedown",
            function (e) {
              this.down = true;
              this.X = e.pageX;
              this.Y = e.pageY;
            },
            0
          );
          canvas.addEventListener(
            "mouseup",
            function () {
              this.down = false;
            },
            0
          );
          canvas.addEventListener(
            "mousemove",
            function (e) {
              if (this.down) {
                with (ctx) {
                  beginPath();
                  moveTo(this.X, this.Y);
                  lineTo(e.pageX, e.pageY);
                  ctx.lineWidth = 1;
                  stroke();
                }
                this.X = e.pageX;
                this.Y = e.pageY;
              }
            },
            0
          );
        </script>
      </div>
    </div>
  </div>
</main>

<style>
  img {
    max-width: 100%;
    max-height: 100%;
    position: relative;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  .main-page {
    height: 100vh;
    width: 100vw;
    background-color: white;
  }

  .header {
    background-color: #d9d9d9;
    height: 6%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
  }

  .icon-name {
    height: 100%;
    width: 33.333%;
    display: flex;
  }
  .icon {
    height: 40px;
    width: 40px;
    border-radius: 4px;
    margin: 4px;
    margin-left: 14px;
  }

  .app-title {
    color: black;
    display: flex;
    align-items: center;
    padding-left: 2%;
    font-size: large;
  }
  .whiteboard-name {
    color: black;
    font-size: x-large;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;

    height: 100%;
    width: 33.333%;
  }

  .user {
    height: 100%;
    width: 33.333%;
    display: flex;
    align-items: center;
    justify-content: end;
  }
  .user-icon {
    height: 40px;
    width: 40px;
    border-radius: 40px;
    background-color: black;
  }
  .user-name {
    padding-left: 5%;
    padding-right: 5%;
    color: black;
  }
  .sign-out {
    color: black;
    padding-right: 10px;
  }

  .center-page {
    height: 94%;
    width: 100%;
    display: flex;
  }
  .tool-bar {
    height: 100%;
    width: 4%;
    background-color: #ededed;

    display: flex;
    align-items: center;
    flex-direction: column;

    color: black;
  }
  .tool-icon {
    height: 5%;
    width: 60%;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    padding: 10px;
  }
  .tool-icon:hover {
    background-color: lightgrey;
  }

  #currentPage{
    background-color: #ededed;
    height: 80%;
    width: 80%;
    color: black;
    border: solid 1px black;
    text-align: center;
  }

  .canvas {
    height: 100%;
    width: 96%;
    overflow: hidden;
  }
  #my-canvas {
    width: 100%;
    height: 100%;
  }
</style>
