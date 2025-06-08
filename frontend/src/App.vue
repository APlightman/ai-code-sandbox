<template>
  <CodeSandbox />
</template>

<script>
import CodeSandbox from "./components/CodeSandbox.vue";

export default {
  name: "App",
  components: {
    CodeSandbox,
  },
};
</script>

<style>
#app {
  height: 100vh;
  margin: 0;
  padding: 0;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  overflow: hidden;
}
</style>
