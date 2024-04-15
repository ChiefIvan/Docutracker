<script lang="ts">
  import { dark, userData, navExpand } from "../../store";
  import { fly } from "svelte/transition";

  import RegisterDocument from "../lib/RegisterDocument.svelte";
  import ScanDocument from "../lib/ScanDocument.svelte";
  import UnverifiedComp from "./UnverifiedComp.svelte";

  export let shortcutData = "Hello from Shortcut Wrapper";
  export let authToken = "";
  export let editData: any;
</script>

<div
  class="shortcut-wrapper"
  class:dark={$dark}
  class:inrease={!$navExpand}
  in:fly={{ x: 1000, duration: 800, delay: 100 }}
  out:fly={{ x: 1000, duration: 800, delay: 100 }}
>
  {#if shortcutData === "Register Document"}
    {#if $userData.full_ver_val}
      <RegisterDocument {authToken} {editData} on:switch></RegisterDocument>
    {:else}
      <UnverifiedComp></UnverifiedComp>
    {/if}
  {:else if shortcutData === "Request Document"}
    <p>Hello</p>
    <!-- {:else}
    {shortcutData} -->
  {:else if shortcutData === "Scan Document"}
    {#if $userData.full_ver_val}
      <ScanDocument {authToken} on:switch on:closeShortCut></ScanDocument>
    {:else}
      <UnverifiedComp></UnverifiedComp>
    {/if}
  {/if}
</div>

<style>
  div.shortcut-wrapper {
    overflow-y: auto;
    transition: background-color ease-in-out 300ms;
    position: absolute;
    top: 3rem;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: var(--main-col-5);
    height: calc(100vh - 43.16px);
    z-index: 2;
  }

  div.shortcut-wrapper::-webkit-scrollbar {
    width: 0.5rem;
    height: 0.5rem;
  }

  div.shortcut-wrapper::-webkit-scrollbar-track {
    background: var(--main-col-6);
  }

  div.shortcut-wrapper::-webkit-scrollbar-thumb {
    background: var(--main-col-3);
  }

  div.shortcut-wrapper::-webkit-scrollbar-thumb:hover {
    background: var(--scroll-color);
  }

  /* div.inrease {
    left: 3.4rem;
  } */

  div.dark {
    background-color: var(--dark-main-col-7);
  }
</style>
