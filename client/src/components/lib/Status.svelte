<script lang="ts">
  import {
    dark,
    documents,
    sortExpand,
    searchArray,
    sortArray,
    userData,
    handleDetails,
    type Document,
  } from "../../store";
  import { tooltip } from "../shared/Tooltip";
  import { afterUpdate } from "svelte";
  import { fade } from "svelte/transition";
  import { flip } from "svelte/animate";

  import TriangleIcon from "../icons/TriangleIcon.svelte";
  import Dropdown from "../shared/Dropdown.svelte";
  import ArrowIcon from "../icons/ArrowIcon.svelte";

  $: console.log(rejectedArrayOr);
  $: console.log($documents);

  let forwardArrayOr: Document[] = [];
  let approvedArrayOr: Document[] = [];
  let waitingArrayOr: Document[] = [];
  let completeArrayOr: Document[] = [];
  let rejectedArrayOr: Document[] = [];

  $: forwardArrayOr = $documents.filter(
    (document) =>
      !document.documentPath.length ||
      (document.documentPath[document.documentPath.length - 1].approved &&
        document.documentPath[document.documentPath.length - 1].confirmed &&
        !document.documentPath[document.documentPath.length - 1].finished &&
        !document.documentPath[document.documentPath.length - 1].complete)
  );

  $: console.log(forwardArrayOr);

  $: approvedArrayOr = $documents.filter(
    (document) =>
      document.documentPath.length &&
      document.documentPath[document.documentPath.length - 1].approved &&
      !document.documentPath[document.documentPath.length - 1].confirmed &&
      !document.documentPath[document.documentPath.length - 1].finished
  );

  $: waitingArrayOr = $documents.filter(
    (document) =>
      document.documentPath.length &&
      document.documentPath[document.documentPath.length - 1].approved &&
      document.documentPath[document.documentPath.length - 1].confirmed &&
      document.documentPath[document.documentPath.length - 1].finished &&
      !document.documentPath[document.documentPath.length - 1].complete
  );

  $: completeArrayOr = $documents.filter(
    (document) =>
      document.documentPath.length &&
      document.documentPath[document.documentPath.length - 1].approved &&
      document.documentPath[document.documentPath.length - 1].confirmed &&
      document.documentPath[document.documentPath.length - 1].finished &&
      document.documentPath[document.documentPath.length - 1].complete
  );

  $: rejectedArrayOr = $documents.filter(
    (document) =>
      document.documentPath.length &&
      !document.documentPath[document.documentPath.length - 1].approved
  );

  let sortName = "Default";
  let searchValue = "";

  $: forwardArray = sortArray(
    searchArray(forwardArrayOr, searchValue),
    sortName
  );
  $: approvedArray = sortArray(
    searchArray(approvedArrayOr, searchValue),
    sortName
  );
  $: completeArray = sortArray(
    searchArray(completeArrayOr, searchValue),
    sortName
  );
  $: waitingArray = sortArray(
    searchArray(waitingArrayOr, searchValue),
    sortName
  );
  $: rejectedArray = sortArray(
    searchArray(rejectedArrayOr, searchValue),
    sortName
  );

  let statusNavigation = "Forwarded";
  let hasDocuments = 0;

  $: {
    if (statusNavigation === "Forwarded") {
      hasDocuments = forwardArray.length;
    } else if (statusNavigation === "Approved") {
      hasDocuments = approvedArray.length;
    } else if (statusNavigation === "Complete") {
      hasDocuments = completeArray.length;
    } else if (statusNavigation === "Waiting") {
      hasDocuments = waitingArray.length;
    } else {
      hasDocuments = rejectedArray.length;
    }
  }

  let openSesame = false;
  const handleCredentials = (document: Document) => {
    console.log(document);
    openSesame = !openSesame;
  };
</script>

<!-- {#if openSesame}
  <div class="credential-wrapper" transition:fade>
    <div class="back-wrapper">
      <ArrowIcon
        arrowState={true}
        sizeMedium={true}
        dark={true}
        on:click={() => (openSesame = false)}
      ></ArrowIcon>
    </div>
    <div class="credentials">

    </div>
  </div>
{/if} -->

<div class="third-wrapper">
  <h2 class="title" class:dark={$dark}>Status</h2>
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
  <ul class="status-nav-wrapper">
    <li
      data-count={forwardArray.length}
      class="nav"
      class:dark={$dark}
      on:click={() => (statusNavigation = "Forwarded")}
      class:active={statusNavigation === "Forwarded"}
      class:empty={!forwardArray.length}
    >
      To Forward
    </li>
    <li
      data-count={approvedArray.length}
      class="nav"
      class:dark={$dark}
      on:click={() => (statusNavigation = "Approved")}
      class:active={statusNavigation === "Approved"}
      class:empty={!approvedArray.length}
    >
      Approved
    </li>
    <li
      data-count={waitingArray.length}
      class="nav"
      class:dark={$dark}
      on:click={() => (statusNavigation = "Waiting")}
      class:active={statusNavigation === "Waiting"}
      class:empty={!waitingArray.length}
    >
      Waiting
    </li>
    <li
      data-count={completeArray.length}
      class="nav"
      class:dark={$dark}
      on:click={() => (statusNavigation = "Complete")}
      class:active={statusNavigation === "Complete"}
      class:empty={!completeArray.length}
    >
      Complete
    </li>
    <li
      data-count={rejectedArray.length}
      class="nav"
      class:dark={$dark}
      on:click={() => (statusNavigation = "Rejected")}
      class:active={statusNavigation === "Rejected"}
      class:empty={!rejectedArray.length}
    >
      Rejected
    </li>
  </ul>

  <section class="content-wrapper">
    <ul class="status-label-wrapper">
      <li>
        <input
          class:dark={$dark}
          type="search"
          placeholder="Search for Documents..."
          bind:value={searchValue}
        />
      </li>
      <!-- svelte-ignore a11y-no-static-element-interactions -->
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <li>
        <div
          class="sort-wrapper"
          class:dark={$dark}
          on:click|stopPropagation={() => ($sortExpand = !$sortExpand)}
          use:tooltip={{
            content: "Sort",
            animation: "perspective-subtle",
            theme: "tooltip",
            arrow: true,
            offset: [0, 15],
          }}
        >
          <span class="sort-name"> {sortName} </span>
          <TriangleIcon
            customDark={true}
            rotate={$sortExpand}
            on:click={() => ($sortExpand = !$sortExpand)}
          ></TriangleIcon>
        </div>
        <Dropdown expand={$sortExpand} status={true}>
          <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
          <li on:click={() => (sortName = "Default")}>
            <span class="mode-name" class:active={sortName === "Default"}
              >Default</span
            >
          </li>
          <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
          <li on:click={() => (sortName = "Date")}>
            <span class="mode-name" class:active={sortName === "Date"}
              >Date</span
            >
          </li>
          <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
          <li on:click={() => (sortName = "Name")}>
            <span class="mode-name" class:active={sortName === "Name"}
              >Name</span
            >
          </li>
        </Dropdown>
      </li>
    </ul>
    {#if hasDocuments}
      <div class="table-wrapper">
        <div class="table" class:dark={$dark}>
          <div class="table-head" class:dark={$dark}>
            <div class="name" class:dark={$dark}>Document Name</div>
            <div class="description" class:dark={$dark}>
              Document Description
            </div>
            <div class:dark={$dark}>Attemps</div>
            <div class:dark={$dark}>Document ID</div>
            {#if statusNavigation === "Forwarded"}
              <div class:dark={$dark}>Registered Date</div>
            {:else if statusNavigation === "Approved"}
              <div class:dark={$dark}>Approved Date</div>
            {:else if statusNavigation === "Confirmed"}
              <div class:dark={$dark}>Confirmed Date</div>
            {/if}
          </div>
          {#if statusNavigation === "Rejected"}
            <div></div>
          {/if}
          <div class="body-wrapper">
            <!-- {#each [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] as count (count)}
              <div
                class="table-body"
                class:dark={$dark}
                use:tooltip={{
                  content: "Click for full details",
                  animation: "perspective-subtle",
                  theme: "tooltip",
                  arrow: true,
                  offset: [0, 15],
                }}
              >
                <div class="name" class:dark={$dark}>Sample</div>
                <div class="description" class:dark={$dark} title={"Sample"}>
                  Sample
                </div>
                <div class="id" class:dark={$dark}>Sample</div>
                <div class="date" class:dark={$dark}>Sample</div>
              </div>
            {/each} -->
            {#if statusNavigation === "Forwarded"}
              {#each forwardArray as document (document.documentID)}
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-no-static-element-interactions -->
                <div
                  class="table-body"
                  class:dark={$dark}
                  use:tooltip={{
                    content: "Click for full details",
                    animation: "perspective-subtle",
                    theme: "tooltip",
                    arrow: true,
                    offset: [0, 15],
                  }}
                  transition:fade
                  animate:flip={{ duration: 500 }}
                  on:click|stopPropagation={() =>
                    handleDetails("", "", $userData.unit, document)}
                >
                  <div
                    class="name"
                    class:dark={$dark}
                    title={document.documentName}
                  >
                    {document.documentName}
                  </div>
                  <div
                    class="description"
                    class:dark={$dark}
                    title={document.documentDescription}
                  >
                    {document.documentDescription}
                  </div>
                  <div class="name" class:dark={$dark} title={document.attemps}>
                    {document.attemps}
                  </div>
                  <div class="id" class:dark={$dark} title={document.codeData}>
                    {document.codeData.slice(0, 5)}
                  </div>
                  <div
                    class="date"
                    class:dark={$dark}
                    title={document.pendingDate}
                  >
                    {document.pendingDate}
                  </div>
                </div>
              {/each}
            {:else if statusNavigation === "Approved"}
              {#each approvedArray as document (document.documentID)}
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-no-static-element-interactions -->
                <div
                  class="table-body"
                  class:dark={$dark}
                  use:tooltip={{
                    content: "Click for full details",
                    animation: "perspective-subtle",
                    theme: "tooltip",
                    arrow: true,
                  }}
                  transition:fade
                  animate:flip={{ duration: 500 }}
                  on:click|stopPropagation={() =>
                    handleDetails("", "", $userData.unit, document)}
                >
                  <div
                    class="name"
                    class:dark={$dark}
                    title={document.documentName}
                  >
                    {document.documentName}
                  </div>
                  <div
                    class="description"
                    class:dark={$dark}
                    title={document.documentDescription}
                  >
                    {document.documentDescription}
                  </div>
                  <div class="name" class:dark={$dark} title={document.attemps}>
                    {document.attemps}
                  </div>
                  <div class="id" class:dark={$dark} title={document.codeData}>
                    {document.codeData.slice(0, 5)}
                  </div>
                  {#each document.documentPath as path, i (i)}
                    <div
                      class="date"
                      class:dark={$dark}
                      title={path.approvedDate}
                    >
                      {path.approvedDate}
                    </div>
                  {/each}
                </div>
              {/each}
            {:else if statusNavigation === "Waiting"}
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <!-- svelte-ignore a11y-no-static-element-interactions -->
              {#each waitingArray as document (document.documentID)}
                <div
                  class="table-body"
                  class:dark={$dark}
                  use:tooltip={{
                    content: "Click for full details",
                    animation: "perspective-subtle",
                    theme: "tooltip",
                    arrow: true,
                  }}
                  transition:fade
                  animate:flip={{ duration: 500 }}
                  on:click|stopPropagation={() =>
                    handleDetails("", "", $userData.unit, document)}
                >
                  <div
                    class="name"
                    class:dark={$dark}
                    title={document.documentName}
                  >
                    {document.documentName}
                  </div>
                  <div
                    class="description"
                    class:dark={$dark}
                    title={document.documentDescription}
                  >
                    {document.documentDescription}
                  </div>
                  <div class="name" class:dark={$dark} title={document.attemps}>
                    {document.attemps}
                  </div>
                  <div class="id" class:dark={$dark} title={document.codeData}>
                    {document.codeData.slice(0, 5)}
                  </div>
                </div>
              {/each}
            {:else if statusNavigation === "Complete"}
              {#each completeArray as document (document.documentID)}
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-no-static-element-interactions -->
                <div
                  class="table-body"
                  class:dark={$dark}
                  use:tooltip={{
                    content: "Click for full details",
                    animation: "perspective-subtle",
                    theme: "tooltip",
                    arrow: true,
                  }}
                  transition:fade
                  animate:flip={{ duration: 500 }}
                  on:click|stopPropagation={() =>
                    handleDetails("", "", $userData.unit, document)}
                >
                  <div
                    class="name"
                    class:dark={$dark}
                    title={document.documentName}
                  >
                    {document.documentName}
                  </div>
                  <div
                    class="description"
                    class:dark={$dark}
                    title={document.documentDescription}
                  >
                    {document.documentDescription}
                  </div>
                  <div class="name" class:dark={$dark} title={document.attemps}>
                    {document.attemps}
                  </div>
                  <div class="id" class:dark={$dark} title={document.codeData}>
                    {document.codeData.slice(0, 5)}
                  </div>
                </div>
              {/each}
            {:else if statusNavigation === "Rejected"}
              {#each rejectedArray as document (document.documentID)}
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-no-static-element-interactions -->
                <div
                  class="table-body"
                  class:dark={$dark}
                  use:tooltip={{
                    content: "Click for full details",
                    animation: "perspective-subtle",
                    theme: "tooltip",
                    arrow: true,
                  }}
                  transition:fade
                  animate:flip={{ duration: 500 }}
                  on:click|stopPropagation={() =>
                    handleDetails("", "", $userData.unit, document)}
                >
                  <div
                    class="name"
                    class:dark={$dark}
                    title={document.documentName}
                  >
                    {document.documentName}
                  </div>
                  <div
                    class="description"
                    class:dark={$dark}
                    title={document.documentDescription}
                  >
                    {document.documentDescription}
                  </div>
                  <div class="name" class:dark={$dark} title={document.attemps}>
                    {document.attemps}
                  </div>
                  <div class="id" class:dark={$dark} title={document.codeData}>
                    {document.codeData.slice(0, 5)}
                  </div>
                </div>
              {/each}
            {/if}
          </div>
        </div>
      </div>
    {:else}
      <h2 class="no-document" class:dark={$dark}>
        You don't have any {statusNavigation} Documents
      </h2>
    {/if}
  </section>
</div>

<style>
  div.third-wrapper {
    /* padding: 1rem; */
    max-width: 1000px;
    margin: auto;
    margin-bottom: 3rem;

    & h2.no-document {
      transition: all ease-in-out 500ms;
      text-align: center;
      margin: 5rem 0;
      font-size: 1.5rem;
      font-weight: 700;
    }

    & h2.title {
      font-size: 1.5rem;
      font-weight: 900;
      color: var(--scroll-color);
      margin-top: 1rem;
      margin-bottom: 1rem;
      transition: all ease-int-out 500ms;
    }

    & h2.dark {
      color: var(--background);
    }

    & ul.status-nav-wrapper {
      text-align: center;

      & li.nav {
        position: relative;
        transition: all ease-in-out 500ms;
        display: inline-block;
        cursor: pointer;
        color: var(--scroll-color);
        padding: 0.3rem 1rem;
        margin: 0 0.3rem;
        border-radius: 0.2rem;
      }

      & li::after {
        content: attr(data-count);
        position: absolute;
        top: -0.8rem;
        right: -0.5rem;
        border-radius: 50%;
        background-color: var(--icon-active-color);
        height: 1.5rem;
        width: 1.5rem;
        color: white;
        font-size: 1rem;
        z-index: 1;
      }

      & li.dark::after {
        background-color: var(--dark-main-col-5);
      }

      & li.empty::after {
        display: none;
      }

      & li.nav:hover {
        background-color: var(--header-color);
      }

      & li.active {
        background-color: var(--component-active);
        color: var(--icon-active-color);
      }

      & li.dark {
        color: var(--icon-dark);
      }

      & li.dark.active {
        background-color: var(--dark-main-col-1);
        color: var(--icon-active-color);
      }

      & li.dark:hover {
        background-color: var(--navigation-hover-dark);
      }
    }

    & section.content-wrapper {
      margin-top: 4rem;

      & ul.status-label-wrapper {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.8rem;
        align-items: center;

        & li {
          display: inline-block;
          position: relative;

          & input {
            border: 1px solid var(--header-color);
            border-radius: 0.2rem;
            background-color: transparent;
            padding: 0 0.5rem;
            height: 2rem;
            transition: hover ease-in-out 500ms;
            outline: none;
            width: 20rem;
            color: var(--scroll-color);
          }

          & input::placeholder {
            font-weight: 700;
            color: var(--scroll-color);
          }

          & input.dark::placeholder {
            color: var(--header-color);
          }

          & input.dark {
            border-color: var(--input-color);
            color: var(--background);
          }

          & input:hover {
            border-color: var(--border-hover-color);
          }

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
      }

      & div.table-wrapper {
        & div.table {
          border: 1px solid var(--main-col-6);
          transition: all ease-in-out 500ms;

          & div.table-head {
            display: flex;
            transition: hover ease-in-out 500ms;
            border-bottom: 1px solid var(--main-col-6);

            & div {
              transition: all ease-in-out 500ms;
              flex: 1;
              font-weight: 700;
              padding: 1rem 0.5rem;
              border-left: 1px solid var(--main-col-6);
              color: var(--main-col-3);
            }

            & div.name {
              border-left: none;
            }

            & div.description {
              flex: 2;
            }

            & div.dark {
              color: var(--background);
              border-left-color: var(--input-color);
            }
          }

          & div.table-head.dark {
            border-color: var(--input-color);
          }

          & div.body-wrapper {
            max-height: 24.5rem;
            overflow-y: auto;

            & div.table-body {
              transition: all ease-in-out 500ms;
              display: flex;

              & div {
                transition: all ease-in-out 300ms;
                flex: 1;
                padding: 0.7rem 0.5rem;
                white-space: nowrap;
                overflow: hidden;
                cursor: pointer;
              }

              & div.dark {
                color: var(--main-col-2);
              }

              & div.name {
                /* flex: 2; */
                border-left: none;
              }

              & div.description {
                -webkit-mask: linear-gradient(90deg, white 50%, transparent);
                mask: linear-gradient(90deg, white 50%, transparent);
                flex: 2;
              }

              & div.id {
                -webkit-mask: linear-gradient(90deg, white 50%, transparent);
                mask: linear-gradient(90deg, white 50%, transparent);
              }

              & div.date {
                -webkit-mask: linear-gradient(90deg, white 50%, transparent);
                mask: linear-gradient(90deg, white 50%, transparent);
              }
            }

            & div.table-body:nth-child(even) {
              background-color: var(--main-col-5);
            }

            & div.table-body.dark:nth-child(even) {
              background-color: var(--dark-main-col-6);
            }

            & div.table-body:hover {
              background-color: var(--header-color);
            }

            & div.table-body.dark:hover {
              background-color: var(--navigation-hover-dark);
            }
          }

          & div.body-wrapper::-webkit-scrollbar {
            width: 0.5rem;
            height: 0.5rem;
          }

          & div.body-wrapper::-webkit-scrollbar-track {
            background: var(--main-col-6);
          }

          & div.body-wrapper::-webkit-scrollbar-thumb {
            background: var(--main-col-3);
          }

          & div.body-wrapper::-webkit-scrollbar-thumb:hover {
            background: var(--scroll-color);
          }
        }

        & div.table.dark {
          border-color: var(--input-color);
        }
      }
    }
  }
</style>
