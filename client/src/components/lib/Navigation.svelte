<script lang="ts">
  import {
    userData,
    navExpand,
    dark,
    location,
    registrationExpand,
  } from "../../store";
  import { navigate } from "svelte-routing";
  import { fade } from "svelte/transition";
  import { createEventDispatcher } from "svelte";

  import ActivityIcon from "../icons/ActivityIcon.svelte";
  import DashboardLogo from "../icons/DashboardIcon.svelte";
  import BellIconNav from "../icons/BellIconNav.svelte";
  import AnalyticsIcon from "../icons/AnalyticsIcon.svelte";
  import OverviewIcon from "../icons/OverviewIcon.svelte";
  import ReportIcon from "../icons/ReportIcon.svelte";

  const dispatch = createEventDispatcher();
  let activeElement = "";

  $: if ($registrationExpand) {
    activeElement = "";
  }

  const closeNav = () => {
    let width = window.innerWidth;

    if (width < 500) {
      $navExpand = false;
    }
  };

  const goToDashboard = () => {
    dispatch("navActive");
    activeElement = "";
    closeNav();
    navigate("/dashboard");
  };

  const goToUpdates = () => {
    dispatch("navActive");
    activeElement = "";
    closeNav();
    navigate("/history");
  };

  const goToNotifications = () => {
    dispatch("navActive");
    activeElement = "";
    closeNav();
    navigate("/notifications");
  };

  const goToReports = () => {
    dispatch("navActive");
    activeElement = "";
    closeNav();
    navigate("/reports");
  };

  const goToAnalytics = () => {
    dispatch("navActive");
    activeElement = "";
    closeNav();
    navigate("/analytics");
  };

  const goToOverview = () => {
    dispatch("navActive");
    activeElement = "";
    closeNav();
    navigate("/document/overview");
  };

  const navigation = [
    {
      id: 1,
      navName: "Dashboard",
      comp: DashboardLogo,
      location: "/dashboard",
      bind: goToDashboard,
    },
    // {
    //   id: 2,
    //   navName: "Notifications",
    //   comp: BellIconNav,
    //   location: "/notifications",
    //   bind: goToNotifications,
    // },
    {
      id: 2,
      navName: "Reports",
      comp: ReportIcon,
      location: "/reports",
      bind: goToReports,
    },
    {
      id: 3,
      navName: "History",
      comp: ActivityIcon,
      location: "/history",
      bind: goToUpdates,
    },
    {
      id: 4,
      navName: "Time Analysis",
      comp: AnalyticsIcon,
      location: "/analytics",
      bind: goToAnalytics,
    },
    // {
    //   id: 5,
    //   navName: "Overview",
    //   comp: OverviewIcon,
    //   location: "/document/overview",
    //   bind: goToOverview,
    // },
  ];

  const scanDocument = () => {
    dispatch("switch", "Scan Document");
    closeNav();
    if (activeElement === "Scan Document") {
      activeElement = "";
      return;
    }

    activeElement = "Scan Document";
  };

  const registerDocument = () => {
    dispatch("switch", "Register Document");
    closeNav();
    if (activeElement === "Register Document") {
      activeElement = "";
      return;
    }

    activeElement = "Register Document";
  };

  const registerRoute = () => {
    dispatch("switch", "Register Route");
    closeNav();
    if (activeElement === "Register Route") {
      activeElement = "";
      return;
    }

    activeElement = "Register Route";
  };

  const updateRoute = () => {
    dispatch("switch", "Update Route");
    closeNav();
    if (activeElement === "Update Route") {
      activeElement = "";
      return;
    }

    activeElement = "Update Route";
  };
</script>

<div class="navigation-wrapper-sidebar">
  {#if $navExpand}
    <span
      class="shortcut-label"
      class:dark={$dark}
      transition:fade={{ duration: 200, delay: 200 }}>Navigation</span
    >
  {/if}
  <ul class="shortcuts">
    {#each navigation as value (value.id)}
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
      <li
        class="shortcut-links"
        class:active={value.location === $location && true}
        class:dark={$dark}
        on:click={value.bind}
      >
        <svelte:component
          this={value.comp}
          compColor={value.location === $location && true}
        ></svelte:component>
        {#if $navExpand}
          <span
            transition:fade={{ duration: 200, delay: 200 }}
            class:dark={$dark}
            class:active={value.location === $location && true}
            class="shortcut-name">{value.navName}</span
          >
        {/if}
      </li>
    {/each}
    <!-- {:else}
      {#each ["FCDSET", "FNAHS", "FGBM"] as ins}
        <li class="shortcut-links" class:dark={$dark}>
          {#if $navExpand}
            <span
              transition:fade={{ duration: 200, delay: 200 }}
              class:dark={$dark}
              class="shortcut-name">{ins}</span
            >
          {/if}
        </li>
      {/each} -->
  </ul>
</div>

<style>
  span.shortcut-label {
    margin-top: 2rem;
    display: inline-block;
    color: var(--scroll-color);
    font-weight: bold;
  }

  span.shortcut-label.dark {
    color: var(--main-col-2);
  }

  div.navigation-wrapper-sidebar {
    & ul.shortcuts {
      margin-top: 1rem;

      & li.shortcut-links {
        transition: background-color ease-in-out 200ms;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border-bottom: 1px solid transparent;
        margin: 0.2rem 0;
        height: 2.2rem;
        padding-left: 0.3rem;
        cursor: pointer;
        border-radius: 0.2rem;

        & span.shortcut-name {
          transition: color ease-in-out 300ms;
          font-size: 0.9rem;
          color: var(--scroll-color);
          display: inline-block;
          text-wrap: nowrap;
        }

        & span.shortcut-name.active {
          color: var(--icon-active-color);
        }

        & span.dark {
          transition: color ease-in-out 300ms;
          color: var(--icon-dark);
        }
      }

      & li.shortcut-links:hover {
        background-color: var(--header-color);
      }

      & li.shortcut-links.active {
        background-color: var(--component-active);
      }

      & li.shortcut-links.active.dark {
        background-color: var(--dark-main-col-2);
      }

      & li.shortcut-links.dark:hover {
        background-color: var(--navigation-hover-dark);
      }
    }

    & ul.navigation {
      transition: all ease-in-out 100ms;
      margin-top: 1rem;
      border-radius: 1rem;
      overflow: hidden;
      border: 1px solid var(--header-color);

      & li.navigation-selection {
        transition: all ease-in-out 300ms;
        cursor: pointer;
        display: flex;
        align-items: center;
        column-gap: 0.1rem;
        padding-left: 1rem;
        height: 2.6rem;
      }

      & li.navigation-selection:hover {
        background-color: var(--header-color);
      }

      & li.navigation-selection.dark:hover {
        background-color: var(--navigation-hover-dark);
      }

      & li.active {
        background-color: var(--component-active);
      }

      & li.active.dark {
        background-color: var(--icon-active-color);
      }

      & span {
        color: var(--scroll-color);
        margin-left: 0.5rem;
        font-size: 1rem;
      }

      & span.dark {
        color: var(--background);
      }

      & span.active {
        color: var(--icon-active-color);
      }

      & span.active.dark {
        color: var(--background);
      }
    }

    & ul.navigation.dark {
      border-color: var(--input-color);
    }
  }
</style>
