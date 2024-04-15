<script lang="ts">
  import {
    location,
    dark,
    userData,
    modeExpand,
    profileExpand,
    registrationExpand,
    showMessage,
    notificationExpand,
    documentSelected,
    handleFetch,
    notificationCount,
    address,
    notifications,
  } from "../../store";
  import { tooltip } from "../shared/Tooltip";
  import { Link, navigate } from "svelte-routing";
  import { fade, fly } from "svelte/transition";
  import { createEventDispatcher } from "svelte";

  import ArrowIcon from "../icons/ArrowIcon.svelte";
  import MediaQuery from "../shared/MediaQuery.svelte";
  import Mode from "../shared/Mode.svelte";
  import UserIcon from "../icons/UserIcon.svelte";
  import Button from "../shared/Button.svelte";
  import userIcon from "../../assets/user-icon.png";
  import BellIcon from "../icons/BellIcon.svelte";
  import BurgerIcon from "../icons/BurgerIcon.svelte";
  import LogoSimple from "./../../assets/transparent-favicons-simple.png";
  import DocumentAvail from "./DocumentAvail.svelte";
  import ScanQrIcon from "../icons/ScanQRIcon.svelte";

  export let verified = false;

  const dispatch = createEventDispatcher();
  const tooltipContent = "Go Back to Overview";

  const handleNavigate = () => {
    navigate("/");
  };

  const handleProfile = () => {
    $profileExpand = !$profileExpand;
    $modeExpand = false;
    $notificationExpand = false;
  };

  const handleNotificationExpand = async () => {
    await handleFetch(
      {
        method: "POST",
        address: `${address}/update_count`,
        credentials: {
          count: $notifications.length,
        },
      },
      sessionStorage.getItem("remember")
    );
    $notificationCount = 0;
    $notificationExpand = !$notificationExpand;
    $profileExpand = false;
    $modeExpand = false;
  };

  const handleScanOpen = () => {
    if (!$userData.full_ver_val) {
      $showMessage = { error: "You must be a fully registered User!" };
      return;
    }

    $documentSelected = "";
    dispatch("switch", "Scan Document");
  };

  $: if ($registrationExpand) {
    document.body.classList.add("disable-scroll");
  } else {
    document.body.classList.remove("disable-scroll");
  }
</script>

<header class="header" class:dark={$dark} class:outside={$location === "/"}>
  <div class="header-container">
    {#if $location === "/auth/login" || $location === "/auth/signup" || $location === "/auth/reset" || $location === "/admin/login" || $location === "/secretary/login"}
      <div
        class="arrow-container"
        use:tooltip={{
          arrow: false,
          content: tooltipContent,
          animation: "perspective-subtle",
          theme: "tooltip",
          offset: [0, 15],
        }}
      >
        <ArrowIcon arrowState={true} dark={true} on:click={handleNavigate} />
      </div>
      <Link to="/terms">
        <span class="terms-link" class:dark={$dark}>Terms</span>
      </Link>
    {:else if $location === "/"}
      <div class="logo">
        <img src={LogoSimple} alt="Docutracker's Logo" />
        <h1 class:dark={$dark}>DOCUTRACKER</h1>
      </div>
      <div class="right-wrapper">
        <Mode />
      </div>
    {:else if $location === "/admin"}
      <div class="logo">
        <h1 class:dark={$dark}>
          <!-- Hello, Admin {$adminUser.length ? $adminUser : "Anonymous"} -->
        </h1>
      </div>
      <Mode />
    {:else if $location === "/dashboard" || $location === "/reports" || $location === "/history" || $location === "/notifications" || $location === "/analytics" || $location === "/document/overview"}
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
      <MediaQuery query="(max-width: 500px)" let:matches>
        {#if matches}
          <BurgerIcon></BurgerIcon>
        {:else if $userData.full_ver_val}
          <DocumentAvail></DocumentAvail>
        {:else}
          <div></div>
        {/if}
      </MediaQuery>
      <div class="utils-wrapper">
        <div class="icon-wrapper">
          {#if $userData.previlage === "User"}
            <MediaQuery query="(min-width: 500px)" let:matches>
              {#if matches}
                <BellIcon
                  compColor={true}
                  on:click={handleNotificationExpand}
                />
              {/if}
            </MediaQuery>
          {:else if $userData.full_ver_val}
            <ScanQrIcon on:click={handleScanOpen}></ScanQrIcon>
          {/if}
          <Mode />
        </div>
        {#if $userData.userImg && $userData.userImg.length !== 0}
          <!-- svelte-ignore a11y-img-redundant-alt -->
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
          <img
            class="user-image-profile"
            on:click|stopPropagation={handleProfile}
            src={$userData.userImg}
            alt="User Profile Picture"
          />
        {:else}
          <UserIcon on:click={handleProfile} />
        {/if}
      </div>
    {/if}
  </div>
</header>

{#if $profileExpand}
  <div
    transition:fade={{ duration: 300, delay: 50 }}
    class="profiles"
    class:not-verified-wrapper={!verified}
    class:dark={$dark}
  >
    <!-- {#if verified} -->
    <div class="upper-wrapper">
      <!-- svelte-ignore a11y-img-redundant-alt -->
      {#if $userData.userImg && $userData.userImg.length !== 0}
        <img
          class="user-placeholder-icon"
          src={$userData.userImg}
          alt="User Profile Picture"
        />
      {:else}
        <img class="user-placeholder-icon" src={userIcon} alt="User Icon" />
      {/if}
      <p
        transition:fly={{ y: -40, duration: 600, delay: 200 }}
        class="email-wrapper"
        class:dark={$dark}
      >
        {$userData.email}
      </p>
      <p
        transition:fly={{ y: -40, duration: 400, delay: 150 }}
        class="name-wrapper"
        class:dark={$dark}
      >
        Hello, {$userData.fullName}!
      </p>
    </div>
    <div class="button-wrapper">
      <h3 class:verified={$userData.full_ver_val}>
        {#if $userData.full_ver_val}
          Verified
        {:else}
          Not Verified
        {/if}
      </h3>
      <MediaQuery query="(max-width: 500px)" let:matches>
        {#if matches}
          <Button on:click={() => {}} critical={true}>Logout</Button>
        {/if}
      </MediaQuery>
    </div>
    <!-- {:else} -->
    <!-- {/if} -->
  </div>
{/if}

<style>
  header.header {
    position: sticky;
    top: 0;
    z-index: 3;
    background-color: var(--main-col-3);
    transition: background-color ease-in-out 400ms;

    & div.header-container {
      padding: 0.5rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: relative;

      & div.arrow-container {
        display: flex;
        align-items: center;
      }

      & span.terms-link {
        text-decoration: none;
        color: var(--header-color);
      }

      & span.terms-link:hover {
        opacity: 0.6;
        text-decoration: underline;
      }

      & div.logo {
        display: flex;
        align-items: center;
        column-gap: 0.5rem;

        & img {
          max-width: 2rem;
        }

        & h1 {
          transition: all ease-in-out 300ms;
          color: var(--scroll-color);
          font-size: 1rem;
          font-weight: bold;
        }

        & h1.dark {
          color: var(--background);
        }
      }

      & div.right-wrapper {
        display: flex;
        align-items: center;
        column-gap: 1.5rem;

        & span.outside {
          color: var(--scroll-color);
          transition: all ease-in-out 300ms;
        }

        & span.outside.dark {
          color: var(--header-color);
        }
      }

      & div.utils-wrapper {
        display: flex;
        align-items: center;
        column-gap: 1rem;

        & div.icon-wrapper {
          display: flex;
          gap: 0.5rem;
        }

        & img.user-image-profile {
          max-width: 2rem;
          border-radius: 50%;
        }

        & img.user-image-profile:hover {
          cursor: pointer;
        }
      }
    }
  }

  header.dark {
    background-color: var(--dark-main-col-6);
  }

  header.outside {
    background-color: transparent;
  }

  div.profiles {
    position: fixed;
    z-index: 2;
    top: 3.5rem;
    right: 0.5rem;
    padding: 1.5rem;
    border-radius: 1rem;
    box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.3);
    background-color: var(--background);
    max-width: 20rem;

    & div.upper-wrapper {
      text-align: center;

      & img.user-placeholder-icon {
        max-width: -webkit-fill-available;
        border-radius: 50%;
      }

      & p.email-wrapper {
        margin: 1rem 0;
        padding: 0.5rem;
        border: 1px solid var(--main-col-6);
        color: var(--scroll-color);
        border-radius: 2rem;
        cursor: pointer;
        transition: background-color ease-in-out 300ms;
      }

      & p.email-wrapper:hover {
        background-color: var(--main-col-6);
      }

      & p.email-wrapper.dark {
        color: var(--background);
        border-color: var(--scroll-color);
      }

      & p.email-wrapper.dark:hover {
        background-color: var(--scroll-color);
      }

      & p.name-wrapper {
        margin-bottom: 0.5rem;
        font-size: 1.3rem;
        color: var(--main-col-3);
      }

      & p.name-wrapper.dark {
        color: var(--background);
      }
    }

    & div.button-wrapper {
      text-align: center;

      & h3 {
        font-size: 2rem;
        font-weight: 900;
        color: var(--forground-color);
      }

      & h3.verified {
        color: var(--border-hover-color);
      }
    }
  }

  div.dark {
    background-color: var(--dark-main-col-1);
  }
</style>
