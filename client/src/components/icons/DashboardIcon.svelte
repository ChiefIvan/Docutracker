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
      stroke-linecap="round"
      stroke-linejoin="round"
      stroke-width="2"
      d="M4 4h6v8H4zm0 12h6v4H4zm10-4h6v8h-6zm0-8h6v4h-6z"
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
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M4 4h6v8H4zm0 12h6v4H4zm10-4h6v8h-6zm0-8h6v4h-6z"
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
