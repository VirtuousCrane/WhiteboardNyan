<script>
  import Icon from "@iconify/svelte";
  import { onMount } from "svelte";

  let whiteboardlogo = "/image/whiteBoardIcon-2.png";

  let canvas, ctx;
  let previousX = Infinity;
  let previousY = Infinity;
  let colorHue = 0;

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
  }

  function paint(e) {
    const { clientX, clientY, offsetX, offsetY } = e;
    ctx.strokeStyle = `hsl(${colorHue}, 100%, 60%)`;
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
    colorHue++;
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
        <div class="tool-icon">
          <Icon icon="fluent-emoji-high-contrast:pencil" width="32" height="32"/>
        </div>
        <div class="tool-icon">
          <Icon icon="icons8:eraser" width="44" height="44" />
        </div>
      </div>
      <div class="canvas">
        <canvas id="my-canvas" bind:this={canvas} on:mousedown={onMouseDown} />
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
    /* border: solid 1px black; */
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
  .tool-icon{
    height: 5%;
    width: 60%;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    padding: 10px;
  }

  .canvas {
    height: 100%;
    width: 96%;
    overflow: hidden;
    /* background-color: red; */
  }
  #my-canvas {
    width: 100%;
    height: 100%;
    /* background-color: red; */
  }
</style>
