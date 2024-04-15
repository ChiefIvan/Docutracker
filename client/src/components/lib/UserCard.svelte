<script lang="ts">
  import {
    dark,
    handleDetails,
    activeTab,
    filterName,
    type Users,
    type Document,
  } from "../../store";
  import { tooltip } from "../shared/Tooltip";
  import { onMount } from "svelte";

  import Self from "./Self.svelte";
  import DocumentCard from "./DocumentCard.svelte";

  export let filteredArray: Users[] = [];

  $: console.log(filteredArray);
  export let route: string = "";

  let documentsExpand = false;
  let user: Users;

  const handleUserDocuments = (selecctedUser: Users) => {
    documentsExpand = true;
    user = selecctedUser
  };
</script>

{#if documentsExpand}
  <DocumentCard {user} on:close={() => documentsExpand = false}></DocumentCard>
{/if}

{#if $filterName === "All"}
  <div class="table">
    {#each filteredArray as user (user.id)}
      <div class="table-head" class:dark={$dark}>
        <div class:dark={$dark}>Author</div>
        <div class:dark={$dark}>Email</div>
        <div class:dark={$dark}>Institue</div>
        <div class:dark={$dark}>Unit/Designation</div>
      </div>
      <!-- svelte-ignore missing-declaration -->
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-static-element-interactions -->
      <div class="table-body" on:click={() => handleUserDocuments(user)}>
        <p class="value img">
          <!-- svelte-ignore a11y-img-redundant-alt -->
          <img src={user.userImg} alt="Author Image" />
          <span class="wrapper">{user.fullName}</span>
        </p>
        <p class="value">{user.email}</p>
        <p class="value">{user.institute}</p>
        <p class="value">{user.designation}</p>
      </div>
     <!-- LeftOver Goes Here -->
    {/each}
  </div>
{:else}
  <Self {route} {filteredArray}></Self>
{/if}

<style>
  div.table {
    & div.table-head {
      display: flex;
      transition: hover ease-in-out 500ms;
      border: 1px solid var(--main-col-6);
      border-radius: 1rem;
      margin-bottom: 0.5rem;

      & div {
        transition: all ease-in-out 500ms;
        flex: 1;
        font-weight: 700;
        padding: 1rem 0.5rem;
        border-left: 1px solid var(--main-col-6);
        color: var(--main-col-3);
      }

      & div.img {
        border-left: none;
      }

      & div.dark {
        color: var(--background);
        border-left-color: var(--input-color);
      }
    }

    & div.table-body {
      display: flex;
      transition: all ease-in-out 300ms;
      border-radius: .5rem;
      margin-bottom: 0.5rem;
      cursor: pointer;
      padding: 0.5rem;

      & p.value {
        transition: all ease-in-out 500ms;
        flex: 1;
        padding: 0 0.5rem;
        color: var(--main-col-3);
      }
    }

    & div.table-body:hover {
      background-color: var(--main-col-6);
    }

    & div.table-body:nth-child(odd) {
      background-color: var(--main-col-5);;
    }

    & div.user-wrapper {
      padding: 0 1rem;
      padding-bottom: 1rem;
      /* border: 1px solid var(--header-color); */
      position: relative;
      border-radius: 1rem;

      & div.credential-wrapper {
        margin-top: 6rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid var(--header-color);

        & p.label {
          color: var(--main-col-7);
          transition: all ease-in-out 300ms;
        }

        /* & p.dark {
          color: var(--main);
        } */
      }

      & div.credential-wrapper.dark {
        border-bottom-color: var(--main-col-1);
      }

      & h3 {
        font-size: 1rem;
        color: var(--scroll-color);
        font-weight: bold;
        margin-top: 1.5rem;
        transition: all ease-in-out 300ms;
      }

      & h3.dark {
        color: var(--background);
      }

      & img {
        max-width: 8rem;
        border-radius: 50%;
        position: absolute;
        top: -4rem;
      }

      & div.document-wrapper {
        display: grid;
        gap: 0.5rem;
        grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
        margin-top: 0.5rem;

        & div.documents {
          background-color: var(--background);
          padding: 20px;
          border-radius: 6px;
          cursor: pointer;
          transition: all ease-in-out 300ms;
          box-shadow: 1px 2px 4px rgba(0, 0, 0, 0.1);
        }

        & div.dark {
          background-color: var(--dark-main-col-5);
          color: var(--background);
        }

        & div.documents:hover {
          scale: 0.95;
        }
      }
    }
  }
</style>
