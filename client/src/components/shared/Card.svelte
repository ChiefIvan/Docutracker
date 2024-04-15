<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="card" on:click>
  <slot />
</div>

<style>
  div.card {
    /* height: 15rem; */
    overflow: hidden;
    width: 100%;
    max-width: 35rem;
    cursor: pointer;
    border-radius: 1rem;
    box-shadow: 3px 4px 6px rgba(0, 0, 0, 0.1);
    transition: all ease-in-out 300ms;
  }

  div.card:hover {
    box-shadow: 5px 5px 25px rgba(0, 0, 0, 0.1);
    scale: 1.05;
  }
</style>
