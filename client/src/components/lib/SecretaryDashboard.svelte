<script lang="ts">
  import {
    handleFetch,
    address,
    dark,
    userData,
    handleDetails,
    detailsExpand,
    users,
    activeTab,
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

  import SecNav from "./SecNav.svelte";
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

  let forwardedDocuments: Users[] = [];
  let approvedDocuments: Users[] = [];
  let rejectedDocuments: Users[] = [];
  let waitingDocuments: Users[] = [];
  let completeDocuments: Users[] = [];

  let orForwardedDocuments: Users[] = [];
  let orApprovedDocuments: Users[] = [];
  let orRejectedDocuments: Users[] = [];
  let orWaitingDocuments: Users[] = [];
  let orCompleteDocuments: Users[] = [];

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

      $users.forEach((user) => {
        let isForwarded = user.documents.some((doc) => {
          if (doc.documentPath && doc.documentPath.length) {
            return (
              doc.documentPath[doc.documentPath.length - 1].approved &&
              doc.documentPath[doc.documentPath.length - 1].confirmed &&
              !doc.documentPath[doc.documentPath.length - 1].finished
            );
          }

          return true;
        });

        if (isForwarded) {
          forwardedDocuments = [...forwardedDocuments, user];
          orForwardedDocuments = [...orForwardedDocuments, user];
        }
      });

      $users.forEach((user) => {
        let hasApproved = user.documents.some((doc) => {
          if (!doc.documentPath.length) return false;
          return (
            doc.documentPath[doc.documentPath.length - 1].approved &&
            !doc.documentPath[doc.documentPath.length - 1].confirmed &&
            !doc.documentPath[doc.documentPath.length - 1].finished
          );
        });

        if (hasApproved) {
          approvedDocuments = [...approvedDocuments, user];
          orApprovedDocuments = [...orApprovedDocuments, user];
        }
      });

      $users.forEach((user) => {
        let isRejected = user.documents.some((doc) => {
          if (!doc.documentPath.length) {
            return false;
          }

          return !doc.documentPath[doc.documentPath.length - 1].approved;
        });

        if (isRejected) {
          rejectedDocuments = [...rejectedDocuments, user];
          orRejectedDocuments = [...orRejectedDocuments, user];
        }
      });

      $users.forEach((user) => {
        let isWaiting = user.documents.some((doc) => {
          if (!doc.documentPath.length) return false;
          return (
            doc.documentPath[doc.documentPath.length - 1].approved &&
            doc.documentPath[doc.documentPath.length - 1].finished &&
            !doc.documentPath[doc.documentPath.length - 1].complete
          );
        });

        if (isWaiting) {
          waitingDocuments = [...waitingDocuments, user];
          orWaitingDocuments = [...orWaitingDocuments, user];
        }
      });

      $users.forEach((user) => {
        let isComplete = user.documents.some((doc) => {
          if (!doc.documentPath.length) return false;
          return (
            doc.documentPath[doc.documentPath.length - 1].approved &&
            !doc.documentPath[doc.documentPath.length - 1].confirmed &&
            doc.documentPath[doc.documentPath.length - 1].finished &&
            doc.documentPath[doc.documentPath.length - 1].complete
          );
        });

        if (isComplete) {
          completeDocuments = [...completeDocuments, user];
          orCompleteDocuments = [...orCompleteDocuments, user];
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
    forwardedDocuments = orForwardedDocuments;
    approvedDocuments = orApprovedDocuments;
    rejectedDocuments = orRejectedDocuments;
    waitingDocuments = orWaitingDocuments;
    completeDocuments = orCompleteDocuments;

    $filterName = name;
    insName = "";
    $sortExpand = false;
  };

  const insFiltername = (name: string) => {
    forwardedDocuments = orForwardedDocuments;
    approvedDocuments = orApprovedDocuments;
    rejectedDocuments = orRejectedDocuments;
    waitingDocuments = orWaitingDocuments;
    completeDocuments = orCompleteDocuments;

    if (insName === name) {
      insName = "";
    } else {
      forwardedDocuments = forwardedDocuments.filter(
        (doc) => doc.institute === name
      );

      approvedDocuments = approvedDocuments.filter(
        (doc) => doc.institute === name
      );

      rejectedDocuments = rejectedDocuments.filter(
        (doc) => doc.institute === name
      );

      waitingDocuments = waitingDocuments.filter(
        (doc) => doc.institute === name
      );

      completeDocuments = completeDocuments.filter(
        (doc) => doc.institute === name
      );
      insName = name;
    }
  };
</script>

<SecNav></SecNav>
{#if $detailsExpand}
  <DocumentModal {authToken} {route}></DocumentModal>
{/if}

<main>
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <!-- svelte-ignore a11y-no-static-element-interactions -->
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
          <span class="mode-name" class:active={sortName === "Date"}>Date</span>
        </li>
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
        <li on:click={() => switchSortname("Name")}>
          <span class="mode-name" class:active={sortName === "Name"}>Name</span>
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
      <span class="sort-name"> {insName.length ? insName : $filterName} </span>
      <TriangleIcon
        customDark={true}
        rotate={$filterExpand}
        on:click={() => {
          $filterExpand = !$filterExpand;
          $sortExpand = false;
        }}
      ></TriangleIcon>
    </div>
    <Dropdown expand={$filterExpand} secretary={true}>
      <h2 class="dropdown-title" class:dark={$dark}>Category</h2>
      <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <li on:click={() => switchFiltername("All")}>
        <span class="mode-name" class:active={$filterName === "All"}>All</span>
      </li>
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
      <li on:click={() => switchFiltername("Self")}>
        <span class="mode-name" class:active={$filterName === "Self"}>Self</span
        >
      </li>
      <h2 class="dropdown-title" class:dark={$dark} style="margin-top: 1rem;">
        Filter
      </h2>
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
      <li on:click={() => insFiltername("FGBM")}>
        <span class="mode-name" class:active={insName === "FGBM"}>FGBM</span>
      </li>
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
      <li on:click={() => insFiltername("FCDSET")}>
        <span class="mode-name" class:active={insName === "FCDSET"}>FCDSET</span
        >
      </li>
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
      <li on:click={() => insFiltername("FNAHS")}>
        <span class="mode-name" class:active={insName === "FNAHS"}>FNAHS</span>
      </li>
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
      <li on:click={() => insFiltername("FALS")}>
        <span class="mode-name" class:active={insName === "FALS"}>FALS</span>
      </li>
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
      <li on:click={() => insFiltername("FTED")}>
        <span class="mode-name" class:active={insName === "FTED"}>FTED</span>
      </li>
    </Dropdown>
  </div>

  {#if $activeTab === "Forward"}
    {#if !forwardedDocuments.length}
      There's no Forwarded Documents yet!
    {:else}
      <UserCard filteredArray={forwardedDocuments} {route}></UserCard>
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
  {/if}
</main>

<style>
  main {
    max-width: 1300px;
    margin: auto;

    & div.filter {
      display: flex;
      justify-content: flex-end;
      position: relative;
      padding: 0 2rem;
      column-gap: 0.5rem;
      margin-bottom: 1.5rem;
      transition: all ease-in-out 500ms;

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
