<script>
  import Icon from "@iconify/svelte";
  import { onMount } from "svelte";

  let RESOURCE_ROOT = "/static/";

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

  onMount(() => {
    initialize();

    return () => {
      // unMount
    };
  });

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
    if (toolSelected == "1") {
      const { clientX, clientY, offsetX, offsetY } = e;
      ctx.strokeStyle = colorHue;
      ctx.beginPath();

      if (
        Math.abs(previousX - clientX) < 100 &&
        Math.abs(previousY - clientY) < 100
      ) {
        ctx.moveTo(previousX, previousY);
      }

      ctx.lineTo(offsetX, offsetY);
      ctx.stroke();
      previousX = offsetX;
      previousY = offsetY;
    } else if (toolSelected == "2") {
      const { clientX, clientY, offsetX, offsetY } = e;
      ctx.strokeStyle = "#ffffff";
      ctx.beginPath();

      if (
        Math.abs(previousX - clientX) < 100 &&
        Math.abs(previousY - clientY) < 100
      ) {
        ctx.moveTo(previousX, previousY);
      }

      ctx.lineTo(offsetX, offsetY);
      ctx.stroke();
      previousX = offsetX;
      previousY = offsetY;
    }
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
          <input type="text" id="currentPage">
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
    width: 4em;
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
