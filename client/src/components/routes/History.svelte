<script lang="ts">
  import {
    documents,
    documentSelected,
    dark,
    sortExpand,
    searchArray,
    sortArray,
    detailsExpand,
    type Document,
  } from "../../store";
  import { onDestroy } from "svelte";
  import { tooltip } from "../shared/Tooltip";
  import { fade } from "svelte/transition";

  import CheckAuthenticity from "../shared/CheckAuthenticity.svelte";
  import Dropdown from "../shared/Dropdown.svelte";
  import TriangleIcon from "../icons/TriangleIcon.svelte";
  import DocumentModal from "../lib/DocumentModal.svelte";
  import DocumentCredentials from "../lib/documentCredentials.svelte";

  export let authToken = "";
  onDestroy(() => ($documentSelected = ""));

  let sortName = "Default";

  $: allDocuments = sortArray(
    searchArray($documents, $documentSelected),
    sortName
  );

  $: allDC = allDocuments.filter((document) => {
    if (
      document.documentPath.length &&
      document.documentPath[document.documentPath.length - 1].complete
    )
      return true;
    return false;
  });

  let left = false;
  let right = false;
  let isOpen = false;
  let document: Document;

  const handleDocumentCredentials = (args: Document) => {
    isOpen = !isOpen;
    document = args;
  };
</script>

<svelte:head>
  <title>DOCUTRACKER | History</title>
</svelte:head>

<CheckAuthenticity {authToken} on:user></CheckAuthenticity>

{#if isOpen}
  <DocumentCredentials theDocument={document} on:close={() => (isOpen = false)}
  ></DocumentCredentials>
{/if}

{#if $detailsExpand}
  <DocumentModal {authToken}></DocumentModal>
{/if}

<main>
  {#if allDC.length}
    <div class="documents-wrapper">
      <!-- svelte-ignore a11y-no-static-element-interactions -->
      <!-- svelte-ignore a11y-mouse-events-have-key-events -->
      <div
        class="left nav"
        class:expand={left}
        on:mouseover={() => (left = true)}
        on:mouseleave={() => (left = false)}
      ></div>
      <!-- svelte-ignore a11y-no-static-element-interactions -->
      <!-- svelte-ignore a11y-mouse-events-have-key-events -->
      <div
        class="right nav"
        class:expand={right}
        on:mouseover={() => (right = true)}
        on:mouseleave={() => (right = false)}
      ></div>
      <div class="title-container">
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div
          class="sort-wrapper"
          class:dark={$dark}
          on:click|stopPropagation={() => ($sortExpand = !$sortExpand)}
        >
          {sortName}
          <TriangleIcon on:click={() => ($sortExpand = !$sortExpand)}
          ></TriangleIcon>
        </div>
        <Dropdown expand={$sortExpand} overview={true}>
          <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <li on:click={() => (sortName = "Default")}>
            <span class="mode-name" class:active={sortName === "Default"}
              >Default</span
            >
          </li>
          <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <li on:click={() => (sortName = "Date")}>
            <span class="mode-name" class:active={sortName === "Date"}
              >Date</span
            >
          </li>
          <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <li on:click={() => (sortName = "Name")}>
            <span class="mode-name" class:active={sortName === "Name"}
              >Name</span
            >
          </li>
        </Dropdown>
      </div>
      <div class="table-head" class:dark={$dark}>
        <h2 class="title-name" class:dark={$dark}>Document Name</h2>
        <h2 class="title-status" class:dark={$dark}>Status</h2>
      </div>
      <ul class="list-wrapper">
        {#if allDC.length}
          {#each allDocuments as document (document.documentID)}
            {#if document.documentPath.length}
              {@const path =
                document.documentPath[document.documentPath.length - 1]}
              <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
              {#if path.approved && path.confirmed && path.finished && path.complete}
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <li
                  use:tooltip={{
                    content: "Click for full details",
                    animation: "perspective-subtle",
                    theme: "tooltip",
                    arrow: true,
                    offset: [0, 15],
                  }}
                  transition:fade
                  class:dark={$dark}
                  on:click|stopPropagation={() =>
                    handleDocumentCredentials(document)}
                >
                  <h2 class="name" class:dark={$dark}>
                    {document.documentName}
                  </h2>
                  <span class="status" class:dark={$dark}> complete </span>
                </li>
              {/if}
            {/if}
          {/each}
        {:else}
          <h1 class:dark={$dark}>No Match</h1>
        {/if}
      </ul>
    </div>
  {:else}
    <h2 class="nothing" class:dark={$dark}>
      You don't have any Completed documents yet!
    </h2>
  {/if}
</main>

<style>
  main {
    overflow: hidden;
    position: relative;
    height: calc(100vh - 43.16px);

    /* margin: auto;
    max-width: 1100px; */
    padding: 0 1rem;

    & h2.nothing {
      transition: all ease-in-out 300ms;
      color: var(--input-color);
      line-height: 75vh;
      text-align: center;
      font-weight: bold;
      font-size: 3rem;
    }

    & h2.nothing.dark {
      color: var(--background);
    }

    & div.documents-wrapper {
      & div.nav {
        position: absolute;
        top: 0;
        bottom: 0;
        background-color: transparent;
        width: 2rem;
        /* -webkit-mask: linear-gradient(90deg, white 10%, transparent);
        mask: linear-gradient(90deg, white 10%, transparent); */
        transition: all ease-in-out 300ms;
      }

      & div.expand {
        width: 20rem;
        background-color: rgba(211, 227, 253, 0.6);
      }

      & div.left {
        left: 0;
        border-top-right-radius: 50%;
        border-bottom-right-radius: 50%;
        z-index: 0;
      }

      & div.left.expand {
        transform: translateX(-5rem);
      }

      & div.right {
        right: 0;
        border-top-left-radius: 50%;
        border-bottom-left-radius: 50%;
        z-index: 0;
      }

      & div.right.expand {
        transform: translateX(5rem);
      }

      & div.title-container {
        display: flex;
        justify-content: flex-end;
        align-items: center;

        & div.sort-wrapper {
          display: flex;
          align-items: center;
          column-gap: 0.3rem;
          cursor: pointer;
          padding: 0.2rem 0.5rem;
          border-radius: 0.3rem;
          transition: all ease-in-out 500ms;
          background-color: var(--component-active);
          color: var(--main-col-3);
          margin: 0.5rem 0;
        }

        & div.sort-wrapper.dark {
          background-color: var(--dark-main-col-1);
          color: var(--header-color);
        }

        & div.sort-wrapper:hover {
          background-color: var(--header-color);
        }

        & div.sort-wrapper.dark:hover {
          background-color: var(--dark-main-col-5);
        }

        & li {
          display: flex;
          align-items: center;
          column-gap: 0.5rem;
          margin: 0.2rem;
          padding: 0.2rem 0.5rem;
          border-radius: 0.4rem;
          transition: all ease-in-out 500ms;
          cursor: pointer;

          & span.mode-name {
            color: var(--main-col-1);
          }

          & span.active {
            color: var(--icon-active-color);
          }
        }

        & li:hover {
          background-color: var(--main-col-2);
        }
      }

      & div.table-head {
        transition: all ease-in-out 300ms;
        display: flex;
        border: 1px solid var(--header-color);
        border-radius: 1rem;

        & h2 {
          font-weight: 700;
          color: var(--main-col-3);
          padding: 1rem 1rem;
          transition: all ease-in-out 300ms;
        }

        & h2.title-name {
          flex: 3;
        }

        & h2.title-status {
          padding-left: 1rem;
          border-left: 1px solid var(--header-color);
          flex: 1;
        }

        & h2.dark {
          color: var(--background);
          border-color: var(--input-color);
        }
      }

      & div.table-head.dark {
        border-color: var(--input-color);
      }

      & ul.list-wrapper {
        & li {
          padding: 0.5rem 1rem;
          transition: all ease-in-out 300ms;

          display: flex;
          cursor: pointer;

          & h2.name {
            flex: 3;
            color: var(--main-col-3);
            transition: all ease-in-out 300ms;
          }

          & h2.name.dark {
            color: var(--main-col-2);
          }

          & span.status {
            padding-left: 1rem;
            flex: 1;
            color: var(--main-col-1);
            transition: all ease-in-out 300ms;
          }

          & span.status.dark {
            color: var(--main-col-2);
          }
        }

        & li:nth-child(even) {
          background-color: var(--main-col-5);
        }

        & li.dark:nth-child(even) {
          background-color: var(--dark-main-col-6);
        }

        & h1 {
          transition: all ease-in-out 300ms;
          color: var(--input-color);
          line-height: 70vh;
          text-align: center;
          font-weight: bold;
          font-size: 3rem;
        }

        & h1.dark {
          color: var(--background);
        }
      }
    }
  }
</style>
