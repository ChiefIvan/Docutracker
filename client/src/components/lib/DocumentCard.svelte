<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { fade } from "svelte/transition";
  import { handleDetails, type Users } from "../../store";

  import DocumentModal from "./DocumentModal.svelte";

  export let user: Users;

  const dispatch = createEventDispatcher();
  const handleClose = () => {
    dispatch("close");
  };

  $: console.log(user);
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<!-- svelte-ignore a11y-click-events-have-key-events -->
<div transition:fade class="overlay" on:click|self={handleClose}>
  <div class="document-wrapper">
    <h1>Documents</h1>
    <hr />
    {#if user && user.documents}
      <ul>
        {#each user.documents as document, i (document.documentID)}
          {@const lastRoute =
            document.documentPath && document.documentPath.length
              ? document.documentPath[document.documentPath.length - 1]
              : 0}
          <!-- svelte-ignore missing-declaration -->
          <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
          <li
            on:click={() =>
              handleDetails(user.fullName, user.email, document, "tab1")}
          >
            <div class="document-name">
              {i+1}. {document.documentName}
            </div>
            <div class="wrapper">
              <div>
                {document.codeData}
              </div>
              <div>
                {document.pendingDate}
              </div>
            </div>
          </li>
        {/each}
      </ul>
    {/if}
  </div>
</div>

<style>
  div.overlay {
    position: fixed;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.7);
    z-index: 4;
    display: flex;
    align-items: center;
    justify-content: center;

    & div.document-wrapper {
      background-color: var(--background);
      max-width: 800px;
      width: 100%;
      height: 60%;
      border-radius: 1rem;
      overflow-y: auto;

      & h1 {
        font-size: 1.5rem;
        padding: 0.5rem;
        font-weight: bold;
      }

      & ul {
        padding: 0.5rem;
        max-width: 100%;

        & li {
          padding: 0.5rem;
          transition: all ease-in-out 300ms;
          display: flex;
          justify-content: space-between;
          border-radius: 0.5rem;
          cursor: pointer;

          & div.wrapper {
            display: flex;
            column-gap: 2rem;
          }
        }

        & li:nth-child(odd) {
          background-color: var(--main-col-5);
        }

        & li:hover {
          background-color: var(--main-col-6);
        }
      }
    }
  }
</style>
