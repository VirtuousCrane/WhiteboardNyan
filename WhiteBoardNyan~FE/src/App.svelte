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
  let currentPage = 1;
  let no_pages = 1;

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

  function resize_page() {
    const temp = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const { x, width, y, height } = canvas.getBoundingClientRect();
    canvas.width = width;
    canvas.height = height;

    ctx = canvas.getContext("2d");
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    ctx.lineWidth = 10;
    ctx.putImageData(temp, 0, 0);
  }

  function resize_page_from_canvas(c) {
    let t_canvas = c;
    let t_ctx = c.getContext("2d");
    const temp = t_ctx.getImageData(0, 0, t_canvas.width, t_canvas.height);
    const { x, width, y, height } = t_canvas.getBoundingClientRect();
    t_canvas.width = width;
    t_canvas.height = height;

    t_ctx = canvas.getContext("2d");
    t_ctx.lineJoin = "round";
    t_ctx.lineCap = "round";
    t_ctx.lineWidth = 10;
    t_ctx.putImageData(temp, 0, 0);
  }

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
    canvas = document.querySelector("#cv-1");
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

  function initialize_canvas() {
    console.log("Initializing Canvas...");
    const { x, width, y, height } = canvas.getBoundingClientRect();
    canvas.width = width;
    canvas.height = height;

    ctx = canvas.getContext("2d");
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    ctx.lineWidth = 10;
  }

  function initialize_draw() {
    ctx = canvas.getContext("2d");
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    ctx.lineWidth = 10;

    resize_page();

    canvas.addEventListener("mousedown", onMouseDown);
    canvas.addEventListener("mouseup", onMouseUp);
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
      event: "DRAW",
      data: {
        action: toolSelected,
        page_no: currentPage,
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
  }

  function onMouseMove(event) {
    paint(event);
  }

  function onMouseDown(event) {
    let current_canvas = document.querySelector("#" + event.target.id);

    current_canvas.addEventListener("mousemove", onMouseMove);
    current_canvas.addEventListener("mouseup", onMouseUp);
  }

  function onMouseUp(event) {
    let current_canvas = document.querySelector("#" + event.target.id);

    current_canvas.removeEventListener("mousemove", onMouseMove);
    current_canvas.removeEventListener("mouseup", onMouseUp);
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
        create_page(true);

        break;
      }
      case "5": {
        // previousIcon.style.backgroundColor = "grey";

        currentPage--;
        if (currentPage < 1) {
            currentPage = 1;
        }
        focus_canvas();
        break;
      }
    }
  }

  function create_page(from_btn) {
        if (from_btn) {
          currentPage++;
          if (currentPage <= no_pages) {
            focus_canvas();
            return;
          }
        }
    
        no_pages++;
        let new_page = document.createElement("canvas");
        let canvas_div = document.querySelector("#canvas-div");

        new_page.setAttribute("id", "cv-" + no_pages);
        new_page.classList.add("canvas-board");

        canvas_div.append(new_page);

        if (from_btn) {
          send({
            event: "NEW_PAGE",
            data: {
              page_no: currentPage,
              userID: userID,
            }
          });
        } else {
          resize_page_from_canvas(new_page);
        }

        focus_canvas();
  }

  // Web Socket functions
  function webSocketInit() {
    console.log("Connected to WebSocket");
  }

  function webSocketClose() {
    console.log("Closed WebSocket Connection");
  }

  function messageHandler(message) {
    let content = JSON.parse(message.data);
    let payload = content.payload;
    let data = payload.data;
    let senderID = data.userID;

    if (senderID == userID) {
        return;
    }

    switch(payload.event) {
      case "MESSAGE":
        console.log(data);
        break;
      case "DRAW":
        drawFromMessage(data);
        break;
      case "ALERT":
        alert(data);
        break;
      case "NEW_PAGE":
        create_page(false);
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
      let cmd_canvas = document.querySelector("#cv-" + messageData.page_no);
      let t_ctx = cmd_canvas.getContext("2d");
      t_ctx.lineJoin = "round";
      t_ctx.lineCap = "round";
      t_ctx.lineWidth = 10;

      t_ctx.strokeStyle = messageData.colorHue;
      t_ctx.beginPath();

      t_ctx.moveTo(messageData.clientX, messageData.clientY);

      t_ctx.lineTo(messageData.offsetX, messageData.offsetY);
      t_ctx.stroke();
    }
    else if(messageData.action == "2"){
      let cmd_canvas = document.querySelector("#cv-" + messageData.page_no);
      let t_ctx = cmd_canvas.getContext("2d");
      t_ctx.lineJoin = "round";
      t_ctx.lineCap = "round";
      t_ctx.lineWidth = 10;

      t_ctx.strokeStyle = messageData.colorHue;
      t_ctx.beginPath();

      t_ctx.moveTo(messageData.clientX, messageData.clientY);

      t_ctx.lineTo(messageData.offsetX, messageData.offsetY);
      t_ctx.stroke();
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

  function focus_canvas() {
    if (currentPage > no_pages) {
      currentPage = no_pages;
    }

    let all_canvas = document.querySelectorAll(".canvas-board");

    for (let i = 0; i < all_canvas.length; i++) {
        all_canvas[i].style.visibility = "hidden";
        all_canvas[i].style.zIndex = "-1";
    }

    let f_canvas = document.querySelector("#cv-" + currentPage);
    f_canvas.style.visibility = "visible";
    f_canvas.style.zIndex = "10";

    canvas = f_canvas;
    initialize_draw();
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
      <div class="whiteboard-name">{roomCode}</div>
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
          <form on:submit|preventDefault={focus_canvas}>
            <input type="number" id="currentPage" bind:value={currentPage}>
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
      <div id="canvas-div" class="canvas">
        <canvas
          id="cv-1"
          class="canvas-board"
          on:mousedown={onMouseDown}
          on:mouseup={onMouseUp}
        />
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

  :global(.behind) {
    z-index: -1;
  }

  :global(.front) {
    z-index: 1;
  }

  :global(.canvas) {
    height: 100%;
    width: 96%;
    overflow: hidden;
  }

  :global(.canvas-board) {
    position: absolute;
    width: 100%;
    height: 100%;
  }
</style>
