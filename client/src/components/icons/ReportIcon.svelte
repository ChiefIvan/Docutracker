<script>
  import { dark, navExpand } from "../../store";
  import { tooltip } from "../shared/Tooltip";
  export let compColor = false;
</script>

{#if $navExpand}
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
    ><path
      class:dark={$dark}
      class:bg={compColor}
      d="M20 8l-6-6H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM9 19H7v-9h2v9zm4 0h-2v-6h2v6zm4 0h-2v-3h2v3zM14 9h-1V4l5 5h-4z"
      fill="currentColor"
    /></svg
  >
{:else}
  <div
    use:tooltip={{
      arrow: false,
      content: "Dashboard",
      animation: "perspective-subtle",
      theme: "tooltip",
      offset: [0, 20],
      placement: "right",
    }}
  >
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
      ><path
        class:dark={$dark}
        class:bg={compColor}
        d="M20 8l-6-6H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM9 19H7v-9h2v9zm4 0h-2v-6h2v6zm4 0h-2v-3h2v3zM14 9h-1V4l5 5h-4z"
        fill="currentColor"
      /></svg
    >
  </div>
{/if}
<style>
  div {
    display: flex;
    align-items: center;
  }

  svg {
    min-width: 1.8rem;
    max-width: 1.8rem;
    cursor: pointer;
    transition: all ease-in-out 500ms;

    & path {
      transition: all ease-in-out 300ms;
      fill: var(--main-col-1);
      stroke: var(--main-col-1);
    }

    & path.dark {
      stroke: var(--background);
      fill: var(--background);
    }

    & path.bg {
      fill: var(--icon-active-color);
      stroke: var(--icon-active-color);
    }
  }
</style>
