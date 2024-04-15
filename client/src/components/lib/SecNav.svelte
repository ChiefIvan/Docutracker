<script lang="ts">
  import {
    documentDetails,
    dark,
    activeTab,
    filterName,
    sortExpand,
  } from "../../store";
  import { flip } from "svelte/animate";
  import { tooltip } from "../shared/Tooltip";

  import TriangleIcon from "../icons/TriangleIcon.svelte";
  import Dropdown from "../shared/Dropdown.svelte";

  let tabs = [
    { tabName: "Forward", filter: "All" },
    { tabName: "Approved", filter: "Self" },
    { tabName: "Approved", filter: "All" },
    { tabName: "Rejected", filter: "All" },
    { tabName: "Rejected", filter: "Self" },
    { tabName: "Waiting", filter: "All" },
    { tabName: "Waiting", filter: "Self" },
    { tabName: "Complete", filter: "All" },
  ];

  $: filterTabs = tabs.filter((tab) => {
    if ($filterName === "Self") {
      $activeTab = "Approved";
      return tab.filter === "Self";
    }

    $activeTab = "Forward";
    return tab.filter === "All";
  });

  let sortName = "Default";
</script>

<div class="tabs" class:dark={$dark}>
  <ul>
    {#each filterTabs as tab, i (i)}
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
      <li
        class="nav"
        animate:flip={{ duration: 500 }}
        on:click={() => {
          $activeTab = tab.tabName;
          $documentDetails.approvedDateD = "";
          $documentDetails.confirmedD = 0;
        }}
        class:active={tab.tabName === $activeTab}
        class:dark={$dark}
      >
        {tab.tabName}
      </li>
    {/each}
  </ul>
</div>

<style>
  div.tabs {
    margin: auto;
    margin-top: 1.5rem;
    max-width: 900px;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--header-color);
    text-align: center;
    transition: all ease-in-out 500ms;

    & ul {
      & li.nav {
        transition: all ease-in-out 500ms;
        display: inline-block;
        cursor: pointer;
        color: var(--scroll-color);
        padding: 0.3rem 1rem;
        margin: 0 0.3rem;
        border-radius: 0.2rem;

        & li:hover {
          background-color: var(--main-col-2);
        }
      }

      & li.nav:hover {
        background-color: var(--header-color);
      }

      & li.nav.active {
        background-color: var(--component-active);
        color: var(--icon-active-color);
      }

      & li.nav.dark {
        color: var(--icon-dark);
      }

      & li.nav.dark.active {
        background-color: var(--dark-main-col-1);
        color: var(--icon-active-color);
      }

      & li.nav.dark:hover {
        background-color: var(--navigation-hover-dark);
      }
    }
  }

  div.dark {
    border-bottom-color: var(--input-color);
  }
</style>
