<script lang="ts">
  import {
    handleFetch,
    address,
    dark,
    userData,
    detailsExpand,
    users,
    filterExpand,
    filterName,
    sortExpand,
    type RequestAPI,
    type ResponseData,
    type Users,
  } from "../../store";
  import { navigate } from "svelte-routing";
  import { onMount, createEventDispatcher, type EventDispatcher } from "svelte";
  import { tooltip } from "../shared/Tooltip";
  import { fade } from "svelte/transition";

  import DocumentModal from "./DocumentModal.svelte";
  import Dropdown from "../shared/Dropdown.svelte";
  import TriangleIcon from "../icons/TriangleIcon.svelte";
  import UserCard from "./UserCard.svelte";

  type EventDispatcher<T> = (eventname: string, eventData: T) => void;
  const dispatch: EventDispatcher<string> = createEventDispatcher();

  // const handleDispatch = (item: string) => {
  //   dispatch("tabChange", item);
  // };

  export let authToken: string;

  const indexAddress = `${address}/get_all`;
  const indexMethod = "GET";

  let insName = "";
  let documents: any[] = [];

  const authRequest: RequestAPI = {
    method: indexMethod,
    address: indexAddress,
  };

  let route: string | undefined;

  async function fetchDataAndDispatch() {
    if (!authToken.length) {
      console.warn("Auth Token is empty");
      navigate("/auth/login");
      return;
    }

    try {
      const response: ResponseData = await handleFetch(authRequest, authToken);

      if (response && response.users) {
        $users = response.users;
        route = response.unit;
      }

      console.log($userData);

      $users.forEach((user) => {
        let isValid = user.documents.some((doc) => {
          if (!doc.documentPath.length) {
            if (
              $userData.unit === "Program Head" &&
              !["Program Head", "Dean Office"].includes(user.unit) &&
              $userData.institute === doc.documentInstitute &&
              $userData.program === doc.documentProgram
            ) {
              if (
                doc.documentName === "Faculty Loading" ||
                doc.documentName === "Requested Subject" ||
                doc.documentName === "Endorsement Form" ||
                doc.documentName === "Application for Leave"
              ) {
                return true;
              }
            }

            if (
              $userData.unit === "Dean Office" &&
              user.designation === "Program Head" &&
              $userData.institute === doc.deanInstitute
            ) {
              if (
                doc.documentName === "Faculty Loading" ||
                doc.documentName === "Requested Subject" ||
                doc.documentName === "Endorsement Form" ||
                doc.documentName === "Application for Leave"
              ) {
                return true;
              }
            }

            return false;
          } else if (doc.documentPath.length) {
            if (
              $userData.unit ===
                doc.documentPath[doc.documentPath.length - 1].name &&
              doc.documentPath[doc.documentPath.length - 1].approved &&
              !doc.documentPath[doc.documentPath.length - 1].confirmed
            ) {
              console.log(doc.documentPath[doc.documentPath.length - 1].name);
              if (
                doc.documentName === "Faculty Loading" ||
                doc.documentName === "Requested Subject" ||
                doc.documentName === "Endorsement Form"
              ) {
                return true;
              }
            }

            if (
              $userData.unit ===
                doc.documentPath[doc.documentPath.length - 1].name &&
              doc.documentPath[doc.documentPath.length - 1].approved &&
              !doc.documentPath[doc.documentPath.length - 1].confirmed
            ) {
              if (
                doc.documentName === "Faculty Loading" ||
                doc.documentName === "Requested Subject" ||
                doc.documentName === "Endorsement Form"
              ) {
                return true;
              }
            }

            if (
              doc.documentPath[doc.documentPath.length - 1].name ===
                "Program Head" &&
              doc.documentPath[doc.documentPath.length - 1].approved &&
              doc.documentPath[doc.documentPath.length - 1].confirmed
            ) {
              if (
                $userData.unit === "Dean Office" &&
                $userData.institute === doc.deanInstitute
              ) {
                if (
                  doc.documentName === "Faculty Loading" ||
                  doc.documentName === "Requested Subject" ||
                  doc.documentName === "Endorsement Form"
                ) {
                  return true;
                }
              }
            }

            if (
              doc.documentPath[doc.documentPath.length - 1].name ===
                "Dean Office" &&
              $userData.institute === doc.deanInstitute &&
              doc.documentPath[doc.documentPath.length - 1].approved &&
              !doc.documentPath[doc.documentPath.length - 1].confirmed
            ) {
              if (
                doc.documentName === "Faculty Loading" ||
                doc.documentName === "Requested Subject" ||
                doc.documentName === "Endorsement Form"
              ) {
                return true;
              }
            }

            if (
              doc.documentPath[doc.documentPath.length - 1].name ===
                "Dean Office" &&
              doc.documentPath[doc.documentPath.length - 1].approved &&
              doc.documentPath[doc.documentPath.length - 1].confirmed
            ) {
              if ($userData.unit === "Academic VP") {
                if (
                  doc.documentName === "Faculty Loading" ||
                  doc.documentName === "Requested Subject" ||
                  doc.documentName === "Endorsement Form"
                ) {
                  return true;
                }
              }
            }

            if (
              doc.documentPath[doc.documentPath.length - 1].name ===
                "Academic VP" &&
              doc.documentPath[doc.documentPath.length - 1].approved &&
              !doc.documentPath[doc.documentPath.length - 1].confirmed
            ) {
              if (
                doc.documentName === "Faculty Loading" ||
                doc.documentName === "Requested Subject" ||
                doc.documentName === "Endorsement Form"
              ) {
                return true;
              }
            }

            console.log(doc.documentPath[doc.documentPath.length - 1]);

            if (
              doc.documentPath[doc.documentPath.length - 1].name ===
                "Academic VP" &&
              doc.documentPath[doc.documentPath.length - 1].approved &&
              doc.documentPath[doc.documentPath.length - 1].confirmed &&
              !doc.documentPath[doc.documentPath.length - 1].finished &&
              !doc.documentPath[doc.documentPath.length - 1].complete
            ) {
              if (
                doc.documentName === "Faculty Loading" ||
                doc.documentName === "Requested Subject"
              ) {
                return true;
              }
            }

            if (
              doc.documentPath[doc.documentPath.length - 1].name ===
                "Academic VP" &&
              doc.documentPath[doc.documentPath.length - 1].approved &&
              doc.documentPath[doc.documentPath.length - 1].confirmed &&
              doc.documentPath[doc.documentPath.length - 1].finished &&
              !doc.documentPath[doc.documentPath.length - 1].complete
            ) {
              if (
                doc.documentName === "Faculty Loading" ||
                doc.documentName === "Requested Subject"
              ) {
                return true;
                console.log("Hello");
              }
            }

            if (
              doc.documentPath[doc.documentPath.length - 1].name ===
                "Academic VP" &&
              doc.documentPath[doc.documentPath.length - 1].confirmed
            ) {
              if ($userData.unit === "OP") {
                if (doc.documentName === "Endorsement Form") {
                  return true;
                }
              }
            }

            if (
              doc.documentPath[doc.documentPath.length - 1].name === "OP" &&
              doc.documentPath[doc.documentPath.length - 1].approved &&
              !doc.documentPath[doc.documentPath.length - 1].confirmed
            ) {
              if (doc.documentName === "Endorsement Form") {
                return true;
              }
            }

            if (
              doc.documentPath[doc.documentPath.length - 1].name === "OP" &&
              doc.documentPath[doc.documentPath.length - 1].approved &&
              doc.documentPath[doc.documentPath.length - 1].confirmed &&
              doc.documentPath[doc.documentPath.length - 1].finished &&
              !doc.documentPath[doc.documentPath.length - 1].complete
            ) {
              if (doc.documentName === "Endorsement Form") {
                return true;
              }
            }
          }

          return false;
        });

        if (isValid) {
          documents = [...documents, user];
        }
      });

      $userData = response;
    } catch (error) {
      navigate("/auth/login");
      console.error(error);
    }
  }

  onMount(async () => {
    await fetchDataAndDispatch();
  });

  let sortName = "Default";

  const switchSortname = (name: string) => {
    sortName = name;
    $filterExpand = false;
  };

  const switchFiltername = (name: string) => {
    // forwardedDocuments = orForwardedDocuments;
    // approvedDocuments = orApprovedDocuments;
    // rejectedDocuments = orRejectedDocuments;
    // waitingDocuments = orWaitingDocuments;
    // completeDocuments = orCompleteDocuments;

    $filterName = name;
    insName = "";
    $sortExpand = false;
  };

  const insFiltername = (name: string) => {
    // forwardedDocuments = orForwardedDocuments;
    // approvedDocuments = orApprovedDocuments;
    // rejectedDocuments = orRejectedDocuments;
    // waitingDocuments = orWaitingDocuments;
    // completeDocuments = orCompleteDocuments;
    // if (insName === name) {
    //   insName = "";
    // } else {
    //   forwardedDocuments = forwardedDocuments.filter(
    //     (doc) => doc.institute === name
    //   );
    //   approvedDocuments = approvedDocuments.filter(
    //     (doc) => doc.institute === name
    //   );
    //   rejectedDocuments = rejectedDocuments.filter(
    //     (doc) => doc.institute === name
    //   );
    //   waitingDocuments = waitingDocuments.filter(
    //     (doc) => doc.institute === name
    //   );
    //   completeDocuments = completeDocuments.filter(
    //     (doc) => doc.institute === name
    //   );
    //   insName = name;
    // }
  };

  let showLogs = false;

  $: logs = $userData.activity;

  let openLogModal = false;
</script>

<!-- <SecNav></SecNav> -->
{#if $detailsExpand}
  <DocumentModal {authToken}></DocumentModal>
{/if}

<button type="button" class="show-logs" on:click={() => (showLogs = !showLogs)}>
  Show Activity Logs
</button>

{#if openLogModal}
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <div
    class="overlay"
    transition:fade
    on:click|self={() => (openLogModal = false)}
  >
    <div class="modal-wrapper"></div>
  </div>
{/if}

<main>
  {#if !showLogs}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    {#if documents && documents.length}
      <div class="filter">
        {#if $filterName === "Self"}
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <div
            class="filter-wrapper"
            transition:fade
            class:dark={$dark}
            on:click|stopPropagation={() => {
              $sortExpand = !$sortExpand;
              $filterExpand = false;
            }}
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
              on:click={() => {
                $sortExpand = !$sortExpand;
                $filterExpand = false;
              }}
            ></TriangleIcon>
          </div>
          <Dropdown expand={$sortExpand} self={true}>
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
            <li on:click={() => switchSortname("Default")}>
              <span class="mode-name" class:active={sortName === "Default"}
                >Default</span
              >
            </li>
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
            <li on:click={() => switchSortname("Date")}>
              <span class="mode-name" class:active={sortName === "Date"}
                >Date</span
              >
            </li>
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
            <li on:click={() => switchSortname("Name")}>
              <span class="mode-name" class:active={sortName === "Name"}
                >Name</span
              >
            </li>
          </Dropdown>
        {/if}
        <div
          class="filter-wrapper"
          class:dark={$dark}
          on:click|stopPropagation={() => {
            $filterExpand = !$filterExpand;
            $sortExpand = false;
          }}
          use:tooltip={{
            content: "Filter",
            animation: "perspective-subtle",
            theme: "tooltip",
            arrow: true,
            offset: [0, 15],
          }}
        >
          <span class="sort-name">
            {insName.length ? insName : $filterName}
          </span>
          <TriangleIcon
            customDark={true}
            rotate={$filterExpand}
            on:click={() => {
              $filterExpand = !$filterExpand;
              $sortExpand = false;
            }}
          ></TriangleIcon>
          <Dropdown expand={$filterExpand} secretary={true}>
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
            <li on:click={() => switchFiltername("All")}>
              <span class="mode-name" class:active={$filterName === "All"}
                >All</span
              >
            </li>
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
            <li on:click={() => switchFiltername("Self")}>
              <span class="mode-name" class:active={$filterName === "Self"}
                >Self</span
              >
            </li>
          </Dropdown>
        </div>
      </div>
      <UserCard filteredArray={documents} {route}></UserCard>
    {:else}
      <h1 class="empty-message" class:dark={$dark}>
        You don't have any transactions yet!
      </h1>
    {/if}

    <!-- {#if $activeTab === "Forward"}
    {#if !forwardedDocuments.length}
      There's no Forwarded Documents yet!
    {:else}
    {/if}
  {:else if $activeTab === "Approved"}
    {#if !approvedDocuments.length}
      There's no Approved Documents yet!
    {:else}
      <UserCard filteredArray={approvedDocuments} {route}></UserCard>
    {/if}
  {:else if $activeTab === "Rejected"}
    {#if !rejectedDocuments.length}
      There's no Rejected Documents yet!
    {:else}
      <UserCard filteredArray={rejectedDocuments} {route}></UserCard>
    {/if}
  {:else if $activeTab === "Waiting"}
    {#if !waitingDocuments.length}
      There's no Waiting Documents yet!
    {:else}
      <UserCard filteredArray={waitingDocuments} {route}></UserCard>
    {/if}
  {:else if $activeTab === "Complete"}
    {#if !completeDocuments.length}
      There's no Completed Documents yet!
    {:else}
      <UserCard filteredArray={completeDocuments} {route}></UserCard>
    {/if}
  {/if} -->
  {:else}
    <h1 class="act">Activity Logs</h1>
    <div class="logs-wrapper">
      {#if logs && logs.length}
        <ul class="logs">
          {#each logs.reverse() as log}
            <li>
              <p>{log.content}</p>
              <p>{log.date}</p>
            </li>
          {/each}
        </ul>
      {:else}
        <h1>You don't have any Logs yet!</h1>
      {/if}
    </div>
  {/if}
</main>

<style>
  h1.empty-message {
    line-height: 80vh;
    text-align: center;
    font-weight: bold;
    font-size: 3rem;
    color: var(--input-color);
    transition: all ease-in-out 300ms;
  }

  & h1.dark {
    color: var(--background);
  }

  button.show-logs {
    border-radius: 5rem;
    padding-inline: 2rem;
    padding-block: 0.5rem;
    position: fixed;
    top: 3.5rem;
    right: 0.5rem;
    background-color: transparent;
    border: 1px solid lightgray;
    transition: all ease-in-out 300ms;
  }

  button.show-logs:hover {
    cursor: pointer;
    background-color: rgb(229, 229, 229);
  }

  /* div.overlay {
    position: fixed;
    inset: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    row-gap: 0.5rem;
    z-index: 11;
    background-color: rgba(0, 0, 0, 0.7);

    & div.modal-wrapper {
      border-radius: 0.5rem;
      max-width: 50rem;
      width: 100%;
      padding: 1rem;
      background-color: var(--background);
    }
  } */

  main {
    max-width: 1300px;
    margin: auto;

    & h1.act {
      font-size: 2rem;
      font-weight: bold;
      margin-top: 3rem;
    }

    & div.logs-wrapper {
      margin-top: 2rem;

      & ul.logs {
        & li {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0.5rem;
          transition: all ease-in-out 300ms;
        }

        & li:hover {
          cursor: pointer;
          background-color: lightgray;
          border-radius: 0.5rem;
        }
      }
    }

    & div.filter {
      display: flex;
      justify-content: flex-end;
      position: relative;
      padding: 0 2rem;
      column-gap: 0.5rem;
      margin-bottom: 1.5rem;
      transition: all ease-in-out 500ms;
      margin-top: 3rem;

      & div.filter-wrapper {
        width: 6rem;
        display: flex;
        align-items: center;
        justify-content: center;
        column-gap: 0.3rem;
        cursor: pointer;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        transition: all ease-in-out 500ms;
        background-color: var(--component-active);
        color: var(--main-col-3);
        margin-top: 1rem;
      }

      & div.filter-wrapper.dark {
        background-color: var(--dark-main-col-1);
        color: var(--header-color);
      }

      & div.filter-wrapper:hover {
        background-color: var(--header-color);
      }

      & div.filter-wrapper.dark:hover {
        background-color: var(--dark-main-col-5);
      }

      & h2.dropdown-title {
        padding: 0.5rem;
        font-weight: bold;
        color: var(--main-col-1);
        transition: all ease-in-out 300ms;
      }

      & h2.dark {
        color: var(--background);
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
</style>
