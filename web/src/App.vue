<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <Treddit msg="treddit"/>
    <Submissions>
    </Submissions>
  </div>
</template>

<script>
import Treddit from './components/Treddit.vue'
import Submissions from './components/Submissions.vue'
// import Submission from './components/Submission.vue'

export default {
  name: 'app',
  components: {
    Treddit, Submissions 
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
