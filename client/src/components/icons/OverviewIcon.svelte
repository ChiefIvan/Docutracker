<script>
  import { dark, navExpand } from "../../store";
  import { tooltip } from "../shared/Tooltip";
  export let compColor = false;
</script>

{#if $navExpand}
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
    ><path
      class:active={compColor}
      class:dark={$dark}
      d="M3 19q-.825 0-1.412-.587T1 17V7q0-.825.588-1.412T3 5h10q.825 0 1.413.588T15 7v10q0 .825-.587 1.413T13 19zm14 0V5h2v14zm4 0V5h2v14z"
    /></svg
  >
{:else}
  <div
    use:tooltip={{
      arrow: false,
      content: "Document Overview",
      animation: "perspective-subtle",
      theme: "tooltip",
      offset: [0, 20],
      placement: "right",
    }}
  >
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
      ><path
        class:active={compColor}
        class:dark={$dark}
        d="M3 19q-.825 0-1.412-.587T1 17V7q0-.825.588-1.412T3 5h10q.825 0 1.413.588T15 7v10q0 .825-.587 1.413T13 19zm14 0V5h2v14zm4 0V5h2v14z"
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
    }

    & path.dark {
      fill: var(--background);
    }

    & path.active {
      fill: var(--icon-active-color);
    }
  }
</style>
