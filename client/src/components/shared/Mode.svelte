<script lang="ts">
  import { beforeUpdate } from "svelte";
  import {
    modeExpand,
    dark,
    profileExpand,
    location,
    notificationExpand,
  } from "../../store";
  import { tooltip } from "./Tooltip";

  import SunIcon from "../icons/SunIcon.svelte";
  import MoonIcon from "../icons/MoonIcon.svelte";
  import SystemIcon from "../icons/SystemIcon.svelte";
  import Dropdown from "./Dropdown.svelte";

  let mode: string | null;

  beforeUpdate(() => {
    mode = localStorage.getItem("mode");
    mode !== "System"
      ? mode !== "Dark"
        ? ($dark = false)
        : ($dark = true)
      : !window.matchMedia("(prefers-color-scheme: dark)").matches
        ? ($dark = false)
        : ($dark = true);
  });

  const enableLight = () => {
    localStorage.setItem("mode", "Light");
    $modeExpand = false;
  };

  const enableDark = () => {
    localStorage.setItem("mode", "Dark");
    $modeExpand = false;
  };

  const enableSystem = () => {
    localStorage.setItem("mode", "System");
    $modeExpand = false;
  };

  const modes = [
    { id: 1, modeName: "Light", comp: SunIcon, bind: enableLight },
    { id: 2, modeName: "Dark", comp: MoonIcon, bind: enableDark },
    { id: 3, modeName: "System", comp: SystemIcon, bind: enableSystem },
  ];

  const openModes = () => {
    $modeExpand = !$modeExpand;
    $profileExpand = false;
    $notificationExpand = false;
  };
</script>

{#each modes as value (value.id)}
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <!-- svelte-ignore a11y-no-static-element-interactions -->

  {#if value.modeName === mode}
    {#if !$modeExpand}
      <div
        use:tooltip={{
          arrow: false,
          content: "Modes",
          animation: "perspective-subtle",
          theme: "tooltip",
          offset: [0, 20],
          placement: "bottom",
        }}
        class="comp-render"
        on:click|stopPropagation={openModes}
      >
        <svelte:component this={value.comp} active={true} />
      </div>
    {:else}
      <div class="comp-render" on:click|stopPropagation={openModes}>
        <svelte:component this={value.comp} active={true} />
      </div>
    {/if}
  {/if}
{/each}

<Dropdown
  expand={$modeExpand}
  outside={$location === "/" || $location === "/admin"}
>
  {#each modes as value (value.id)}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
    <li on:click={value.bind}>
      <svelte:component
        this={value.comp}
        active={value.modeName === mode && true}
      />
      <span class="mode-name" class:active={value.modeName === mode && true}
        >{value.modeName}</span
      >
    </li>
  {/each}</Dropdown
>

<style>
  div.comp-render {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  li {
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

  li:hover {
    background-color: var(--main-col-2);
  }
</style>
