<template>
  <div class="home">
  <player />
  </div>
</template>

<script>
import Player from "@/components/Player.vue";
export default {
  components:{
    Player
  }
}
</script>

<style lang="scss">
.home{

  position: relative;
  z-index: 0;
  display: flex;
  justify-content: center;
  align-content: center;
  top: 60px;
  width: 100%;
  height: 600px;
  background-color: #ffedff;
}
</style>