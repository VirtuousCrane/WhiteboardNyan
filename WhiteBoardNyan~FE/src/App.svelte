<script>
  // import svelteLogo from './assets/svelte.svg'
  // import Counter from './lib/Counter.svelte'
  import Icon from '@iconify/svelte';
</script>

<main>
  <div class="main-page">
    <div class="header">
      <div class="icon-name">
        <div class="icon">
          <!-- <img/> -->
          Icon
        </div>
        <div class="app-title">Cooperative Whiteboard</div>
      </div>
      <div class="whiteboard-name">Whiteboard Title</div>
      <div class="user">
        <div class="user-icon">
          <!-- <img/> -->
        </div>
        <div class="user-name">UserTEMP</div>
        <!-- <div class="sign-out"></div> -->
      </div>
    </div>

    <div class="tool-bar">

    </div>

  </div>
</main>

<style>
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
  background-color: rgb(76, 76, 76);
  border-radius: 8px;
  margin: 4px;
  margin-left: 12px;
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
.tool-bar{
  height: 94%;
  width: 64px;
  background-color: #EDEDED;
}
</style>
