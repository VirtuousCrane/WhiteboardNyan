<script>
  // import Counter from './lib/Counter.svelte'
  import Icon from '@iconify/svelte';
  let whiteboardlogo = "/image/whiteBoardIcon-2.png";
</script>

<main>
  <div class="main-page">
    <div class="header">
      <div class="icon-name">
        <div class="icon">
          <img src={whiteboardlogo} alt="whiteboardlogo"/>
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
      <div class="tool-bar"></div>
      <div class="canvas"></div>
    </div>
  </div>
</main>

<style>
img{
  max-width: 100%;
  max-height: 100%;
  position: relative;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.main-page{
  height: 100vh;
  width: 100vw;
  background-color: white;
}

.header{
  background-color: #D9D9D9;
  height: 6%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-evenly;
}

.icon-name{
  height: 100%;
  width: 33.333%;
  display: flex;
}
.icon{
  height: 40px;
  width: 40px;
  border-radius: 4px;
  margin: 4px;
  margin-left: 14px;
  /* border: solid 1px black; */
}

.app-title{
  color: black;
  display: flex;
  align-items: center;
  padding-left: 2%;
  font-size: large;
}
.whiteboard-name{
  color: black;
  font-size: x-large;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;

  height: 100%;
  width: 33.333%;
}

.user{
  height: 100%;
  width: 33.333%;
  display: flex;
  align-items: center;
  justify-content: end;
}
.user-icon{
  height: 40px;
  width: 40px;
  border-radius: 40px;
  background-color: black;
}
.user-name{
  padding-left: 5%;
  padding-right: 5%;
  color: black;
}
.sign-out{
  color: black;
  padding-right: 10px;
}

.center-page{
  height: 94%;
  width: 100%;
  display: flex;
}
.tool-bar{
  height: 100%;
  width: 4%;
  background-color: #EDEDED;
}
.canvas{
  height: 100%;
  width: 96%;
  background-color: red;
}
</style>
