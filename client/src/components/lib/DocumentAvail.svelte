<script lang="ts">
  import {
    dark,
    documents,
    documentSelected,
    theDocument,
    location,
    searchArray,
    appDate,
    comDate,
  } from "../../store";

  let focused = false;

  $: filteredDocuments = searchArray($documents, $documentSelected);
</script>

<!-- <Search hideLabel bind:value></Search> -->
<!-- svelte-ignore a11y-mouse-events-have-key-events -->
<input
  class:input={$documentSelected.length}
  class:not-dashboard={$location === "/history"}
  type="search"
  bind:value={$documentSelected}
  placeholder="Search for Documents..."
  on:mouseover={() => (focused = true)}
  on:mouseout={() => (focused = false)}
/>

{#if $location !== "/history"}
  {#if $documentSelected.length}
    <div
      class="search-wrapper"
      class:dark={$dark}
      class:focused
      class:input={$documentSelected.length}
    >
      <ul>
        {#if $documentSelected.length && filteredDocuments.length}
          <p>Result:</p>
          <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
          <!-- svelte-ignore a11y-click-events-have-key-events -->

          {#each filteredDocuments as value (value.documentID)}
            <li
              on:click={() => {
                localStorage.setItem("docN", value.documentName);
                localStorage.setItem("docid", value.codeData);

                $theDocument = { name: value.documentName, id: value.codeData };
                $documentSelected = "";

                window.location.reload();
              }}
              class:dark={$dark}
            >
              {value.documentName}
            </li>
          {/each}
        {:else}
          <p class="result">No result</p>
        {/if}
      </ul>
    </div>
  {/if}
{/if}

<style>
  input {
    border: 1px solid var(--main-col-1);
    border-radius: 1rem;
    background-color: transparent;
    padding: 0 1rem;
    height: 2rem;
    transition: hover ease-in-out 300ms;
    outline: none;
    width: 20rem;
    color: var(--background);
  }

  input.input {
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
    border-bottom: none;
  }

  input.not-dashboard {
    border-bottom-left-radius: 1rem;
    border-bottom-right-radius: 1rem;
    border: 1px solid var(--main-col-1);
  }

  input::placeholder {
    font-weight: 700;
    color: var(--header-color);
  }

  input:hover {
    border-color: var(--border-hover-color);
  }

  div.search-wrapper {
    transition: all ease-in-out 300ms;
    width: 20rem;
    position: absolute;
    top: 2.4rem;
    z-index: 3;
    left: 1.5rem;
    background-color: var(--main-col-3);
    border: 1px solid var(--main-col-1);
    border-top: 0;
    border-radius: 0.8rem;

    & ul {
      margin-top: 0.5rem;

      & p {
        margin-left: 0.7rem;
        margin-top: 1rem;
        font-weight: 700;
        font-size: 1rem;
        color: var(--background);
      }

      & li {
        color: var(--header-color);
        margin: 0.2rem;
        padding: 0.2rem 0.5rem;
        border-radius: 0.5rem;
        transition: all ease-in-out 500ms;
        cursor: pointer;
      }

      & li::marker {
        color: transparent;
      }

      & li:hover {
        background-color: var(--main-col-2);
        color: var(--scroll-color);
      }

      & li.dark:hover {
        background-color: var(--navigation-hover-dark);
        color: var(--icon-active-color);
      }

      & li:hover::marker {
        color: var(--scroll-color);
      }

      & li.dark:hover::marker {
        color: var(--dark-main-col-1);
      }

      & p.result {
        text-align: center;
        margin: 0;
      }
    }
  }

  div.focused {
    border-color: var(--border-hover-color);
  }

  div.input {
    border-top-right-radius: 0;
    border-top-left-radius: 0;
  }

  div.dark {
    background-color: var(--dark-main-col-6);
  }
</style>
