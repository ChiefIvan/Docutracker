<script lang="ts">
  import { Router, Route } from "svelte-routing";
  import {
    location,
    showMessage,
    notificationExpand,
    registrationExpand,
    dark,
    userData,
  } from "./store";
  import { fly } from "svelte/transition";

  import Overview from "./components/routes/Overview.svelte";
  import Login from "./components/routes/Login.svelte";
  import Signup from "./components/routes/Signup.svelte";
  import Reset from "./components/routes/Reset.svelte";
  import Dashboard from "./components/routes/Dashboard.svelte";
  import Updates from "./components/routes/History.svelte";
  import NavigationLocation from "./components/lib/NavigationLocation.svelte";
  import _Error from "./components/routes/Error.svelte";
  import DisplayMessage from "./components/lib/ShowMessage.svelte";
  import Footer from "./components/lib/Footer.svelte";
  import Header from "./components/lib/Header.svelte";
  import DomEvents from "./components/lib/DOMEvents.svelte";
  import SideBar from "./components/lib/SideBar.svelte";
  import UserRegistration from "./components/lib/UserRegistration.svelte";
  import Notification from "./components/routes/Notification.svelte";
  import Analytics from "./components/routes/Analytics.svelte";
  // import DocumentOverview from "./components/routes/DocumentOverview.svelte";
  import ShortcutWrapper from "./components/shared/ShortcutWrapper.svelte";
  import SuperUserLogin from "./components/routes/SuperUserLogin.svelte";
  import AdminInterface from "./components/routes/AdminInterface.svelte";
  import Reports from "./components/routes/Reports.svelte";

  let show: boolean = false;
  let id: string | number | NodeJS.Timeout | undefined;

  const authToken = sessionStorage.getItem("remember") || "";

  $: if (Object.keys($showMessage).length !== 0) {
    clearTimeout(id);
    show = true;

    id = setTimeout(() => {
      show = false;
    }, 8000);
  }

  let registerD = false;
  let registerR = false;
  let scanD = false;

  let shortcutData: string = "";
  let editData: any;

  const handleShortcutData = (event: { detail: string }) => {
    shortcutData = event.detail;

    if (shortcutData === "Register Document") {
      registerD = !registerD;
      registerR = false;
    }

    if (shortcutData === "Register Route") {
      registerD = false;
      registerR = !registerR;
    }

    if (shortcutData === "Scan Document") {
      scanD = !scanD;
    }
  };

  const handleEdit = (event: {
    detail: {
      documentName: string;
      codeData: string;
      documentDescription: string;
      isEdit: boolean;
    };
  }) => {
    editData = event.detail;
  };

  const handleNavigation = () => {
    registerD = false;
    registerR = false;
  };

  $: if ($registrationExpand) {
    registerD = false;
    registerR = false;
    scanD = false;
  }

  $: if (registerD || registerR) {
    document.body.classList.add("disable-scroll");
    window.scrollTo(0, 0);
  } else {
    document.body.classList.remove("disable-scroll");
  }

  $: console.log($userData);
</script>

{#if show}
  <DisplayMessage responseMessage={$showMessage} />
{/if}

<Router basepath="/">
  <div class="side-main-wrapper">
    {#if $userData.previlage === "User"}
      {#if $location === "/dashboard" || $location === "/reports" || $location === "/history" || $location === "/notifications" || $location === "/analytics" || $location === "/document/overview"}
        <SideBar
          on:switch={handleShortcutData}
          on:navActive={handleNavigation}
        />
      {/if}
    {/if}

    <div class="main-wrapper">
      <DomEvents />
      <Header on:switch={handleShortcutData} />

      {#if $registrationExpand}
        <UserRegistration />
      {/if}

      <Route path="" component={_Error} />
      <Route path="/" component={Overview} />
      <Route path="/admin">
        <AdminInterface {authToken}></AdminInterface>
      </Route>
      <Route path="/dashboard">
        <Dashboard
          on:switch={handleShortcutData}
          on:edit={handleEdit}
          {authToken}
        />
      </Route>
      <Route path="/reports">
        <Reports />
      </Route>
      <!-- {#if $userData.previlage === "User"} -->
      <Route path="/history">
        <Updates {authToken}></Updates>
      </Route>
      <!-- <Route path="/notifications">
          <Notification {authToken}></Notification>
        </Route> -->
      <Route path="/analytics">
        <Analytics {authToken}></Analytics>
      </Route>
      <!-- <Route path="/document/overview">
          <DocumentOverview {authToken}></DocumentOverview>
        </Route> -->
      <!-- {/if} -->
      <Route path="/admin/login" component={SuperUserLogin} />
      <!-- <Route path="/secretary/login" component={SuperUserLogin} /> -->
      <Route path="/auth/login" component={Login} />
      <Route path="/auth/signup" component={Signup} />
      <Route path="/auth/reset" component={Reset} />
      {#if $notificationExpand}
        <div
          in:fly={{ x: 200, duration: 300, delay: 100 }}
          out:fly={{ x: 200, duration: 300, delay: 100 }}
          class="notification-wrapper"
          class:dark={$dark}
        >
          <Notification></Notification>
        </div>
      {/if}

      {#if registerD}
        <ShortcutWrapper
          {shortcutData}
          {authToken}
          {editData}
          on:switch={() => {
            {
              registerD = false;
              shortcutData = "";
            }
          }}
        ></ShortcutWrapper>
      {/if}

      {#if registerR}
        <ShortcutWrapper {shortcutData} {editData} {authToken}
        ></ShortcutWrapper>
      {/if}

      {#if scanD}
        <ShortcutWrapper
          {shortcutData}
          {authToken}
          {editData}
          on:closeShortCut={() => (scanD = false)}
        ></ShortcutWrapper>
      {/if}
      <NavigationLocation />
    </div>
  </div>
</Router>

{#if $location === "/auth/login" || $location === "/auth/signup" || $location === "/auth/reset" || $location === "/admin/login" || $location === "/secretary/login"}
  <Footer />
{/if}

<style>
  div.side-main-wrapper {
    display: flex;

    & div.main-wrapper {
      position: relative;
      width: 100%;

      & div.notification-wrapper {
        transition: background-color ease-in-out 300ms;
        position: fixed;
        z-index: 3;
        top: 3rem;
        right: 0;
        background-color: var(--main-col-5);
        height: 95vh;
        width: 15rem;
      }

      & div.notification-wrapper.dark {
        background-color: var(--dark-main-col-5);
      }
    }
  }
</style>
