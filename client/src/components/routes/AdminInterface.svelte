<script lang="ts">
  import {
    dark,
    handleFetch,
    address,
    userData,
    sortExpand,
    actionExpand,
    type Users,
  } from "../../store";
  import { tooltip } from "../shared/Tooltip";
  import { fade } from "svelte/transition";

  import CheckAuthenticity from "../shared/CheckAuthenticity.svelte";
  import Dropdown from "../shared/Dropdown.svelte";
  import moment from "moment";
  import TriangleIcon from "../icons/TriangleIcon.svelte";
  import ArrowIcon from "../icons/ArrowIcon.svelte";

  export let authToken: string;
  let sortName = "Default";

  const searchArray = (array: Users[], searchTerm: string): Users[] => {
    if (array && array.length) {
      return array.filter((item) => {
        const lowerCasedSearchTerm = searchTerm.toLowerCase();

        return (
          item.institute.toLowerCase().includes(lowerCasedSearchTerm) ||
          item.fullName!.toLowerCase().includes(lowerCasedSearchTerm) ||
          item.email.toLowerCase().includes(lowerCasedSearchTerm) ||
          item.employeeID!.toLowerCase().includes(lowerCasedSearchTerm) ||
          item.unit!.toLowerCase().includes(lowerCasedSearchTerm)
        );
      });
    } else return array;
  };

  const sortArray = (array: Users[], sortName: string): Users[] => {
    if (sortName === "Username") {
      return array.sort((a, b) => a.user_name.localeCompare(b.user_name));
    }

    if (sortName === "Fullname") {
      return array.sort((a, b) => a.fullName!.localeCompare(b.fullName!));
    }

    if (sortName === "Registered Date") {
      return array.sort(
        (a, b) =>
          moment(b.registeredDate).valueOf() -
          moment(a.registeredDate).valueOf()
      );
    }

    return array;
  };

  let searchValue = "";

  $: filteredUser = sortArray(
    searchArray($userData.users!, searchValue),
    sortName
  );

  let openSesame = false;
  let selectedUser: Users;

  const handleUser = (user: Users) => {
    openSesame = !openSesame;
    selectedUser = user;
  };

  const adminRequest = {
    method: "POST",
    address: `${address}/get_users`,
    credentials: { email: "", previlage: "" },
  };

  const handleVerification = async (previlage: string, user: Users) => {
    let selectedPrevilage = "";
    selectedUser = user;

    if (previlage === selectedUser.previlage) {
      return;
    }

    if (previlage === "User") {
      selectedPrevilage = previlage;
    }

    if (previlage === "Secretary") {
      selectedPrevilage = previlage;
    }

    adminRequest.credentials.email = selectedUser.email;
    adminRequest.credentials.previlage = selectedPrevilage;

    try {
      await handleFetch(adminRequest, authToken);
      location.reload();
      console.log($userData.users);
    } catch (error) {
      console.error(error);
    }
  };

  const handleActionExpand = (userID: number) => {
    filteredUser = filteredUser.map((user) => {
      if (user.id === userID) {
        if (!user.open) {
          return { ...user, open: true };
        }
        delete user.open;
      } else {
        delete user.open;
      }
      return user;
    });
  };

  const close = () => {
    filteredUser = filteredUser.map((user) => {
      if (user.open) {
        delete user.open;
      }
      return user;
    });
  };
</script>

<svelte:head>
  <title>DOCUTRACKER | Admin</title>
</svelte:head>

<svelte:window on:scroll={close} on:resize={close} on:click={close} />

<CheckAuthenticity
  {authToken}
  CheckAdminAuthenticityAddress={`${address}/get_users`}
  redirect="/admin/login"
></CheckAuthenticity>

{#if openSesame}
  <!-- svelte-ignore a11y-no-static-element-interactions -->

  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div
    class="details-wrapper"
    transition:fade
    on:click|self={() => (openSesame = false)}
  >
    <div class="arrow-wrapper">
      <ArrowIcon
        arrowState={true}
        sizeMedium={true}
        dark={true}
        on:click={() => (openSesame = !openSesame)}
      ></ArrowIcon>
    </div>
    <div class="details">
      <img src={selectedUser.userImg} alt="User Image" />
      <div class="credentials">
        <h1>User Profile</h1>
        <!-- <div class="credential">
          <h2>User Name</h2>
          <p>{selectedUser.user_name}</p>
        </div> -->
        <div class="credential">
          <h2>Full Name</h2>
          <p>{selectedUser.fullName}</p>
        </div>
        <div class="credential">
          <h2>Email</h2>
          <p>{selectedUser.email}</p>
        </div>
        <div class="credential">
          <h2>Privilage</h2>
          <p>{selectedUser.previlage}</p>
        </div>
        <div class="credential">
          <h2>Unit/Designation</h2>
          <p>{selectedUser.unit}</p>
        </div>
        <div class="credential">
          <h2>Verified</h2>
          <p>{selectedUser.full_ver_val}</p>
        </div>
        <div class="credential">
          <h2>Registered Date</h2>
          <p>{selectedUser.registeredDate}</p>
        </div>
        <!-- <h1>Verified As</h1>
        <div class="button-wrapper">
          <button
            data-content={selectedUser.previlage === "None" ? "✅" : ""}
            on:click|stopPropagation={() => handleVerification("None")}
          >
            None
          </button>
          <button
            data-content={selectedUser.previlage === "User" ? "✅" : ""}
            on:click|stopPropagation={() => handleVerification("User")}
          >
            User
          </button>
          <button
            data-content={selectedUser.previlage === "Secretary" ? "✅" : ""}
            on:click|stopPropagation={() => handleVerification("Secretary")}
          >
            Secretary
          </button>
        </div> -->
      </div>
    </div>
  </div>
{/if}

<main>
  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <div class="search-sort-wrapper">
    <input
      class:dark={$dark}
      type="search"
      placeholder="Search for Users..."
      bind:value={searchValue}
    />
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div
      class="sort-wrapper"
      class:dark={$dark}
      on:click|stopPropagation={() => {
        $sortExpand = !$sortExpand;
        $actionExpand = false;
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
          $actionExpand = false;
        }}
      ></TriangleIcon>
    </div>
    <Dropdown expand={$sortExpand} admin={true}>
      <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <li on:click={() => (sortName = "Default")}>
        <span class="mode-name" class:active={sortName === "Default"}
          >Default</span
        >
      </li>
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
      <!-- <li on:click={() => (sortName = "Username")}>
        <span class="mode-name" class:active={sortName === "Username"}
          >User Name</span
        >
      </li> -->
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
      <li on:click={() => (sortName = "Fullname")}>
        <span class="mode-name" class:active={sortName === "Fullname"}
          >Full Name</span
        >
      </li>
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
      <li on:click={() => (sortName = "Registered Date")}>
        <span class="mode-name" class:active={sortName === "Registered Date"}
          >Registered Date</span
        >
      </li>
    </Dropdown>
  </div>
  {#if filteredUser && filteredUser.length}
    <div class="table-wrapper">
      <div class="table" class:dark={$dark}>
        <div class="table-head" class:dark={$dark}>
          <div class="full-name row" class:dark={$dark}>Fullname</div>
          <div class:dark={$dark} class="row">Employee ID</div>
          <div class:dark={$dark} class="row">Unit/Designation</div>
          <div class:dark={$dark} class="row">Signed In Date</div>
          <div class:dark={$dark} class="row previlage">Privilage</div>
          <div style="flex: 1;"></div>
        </div>
        <div class="body-wrapper">
          {#if filteredUser && filteredUser.length}
            {#each filteredUser as user (user.id)}
              {#if user.emailConfirmed}
                <div class="table-body" class:dark={$dark} transition:fade>
                  <!-- svelte-ignore a11y-click-events-have-key-events
              svelte-ignore a11y-no-static-element-interactions -->
                  <div
                    class="user-cre-row"
                    class:dark={$dark}
                    use:tooltip={{
                      content: "Click for full details",
                      animation: "perspective-subtle",
                      theme: "tooltip",
                      arrow: true,
                      offset: [0, 15],
                    }}
                    on:click={() => handleUser(user)}
                  >
                    <div
                      class="user-name row-cre"
                      class:dark={$dark}
                      title={user.fullName}
                    >
                      <img src={user.userImg} alt="Author Image" />
                      <span class="wrapper">{user.fullName}</span>
                    </div>
                    <div
                      class="doc-name row-cre"
                      class:dark={$dark}
                      title={user.employeeID}
                    >
                      {user.employeeID}
                    </div>
                    <div class:dark={$dark} class="row-cre" title={user.unit}>
                      {user.unit}
                    </div>
                    <div
                      class:dark={$dark}
                      class="row-cre"
                      title={user.registeredDate}
                    >
                      {user.registeredDate}
                    </div>
                    <div
                      class:dark={$dark}
                      class="row-cre"
                      title={user.previlage}
                    >
                      {user.previlage}
                    </div>
                  </div>
                  <div class="action-wrapper" class:dark={$dark}>
                    <!-- svelte-ignore a11y-click-events-have-key-events -->
                    <!-- svelte-ignore a11y-no-static-element-interactions -->

                    <div
                      class="action"
                      on:click|stopPropagation={() =>
                        handleActionExpand(user.id)}
                    >
                      <span> Action </span>
                      <TriangleIcon
                        customDark={true}
                        rotate={user.open ? user.open : false}
                        on:click={() => handleActionExpand(user.id)}
                      ></TriangleIcon>
                      <Dropdown
                        expand={user.open ? user.open : false}
                        admin={true}
                      >
                        <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
                        <!-- svelte-ignore a11y-click-events-have-key-events -->

                        <!-- svelte-ignore a11y-click-events-have-key-events -->
                        <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
                        <li
                          on:click|stopPropagation={() =>
                            handleVerification("User", user)}
                        >
                          <span
                            class="mode-name"
                            class:active={user.previlage === "User"}>User</span
                          >
                        </li>
                        <!-- svelte-ignore a11y-click-events-have-key-events -->
                        <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
                        <li
                          on:click|stopPropagation={() =>
                            handleVerification("Secretary", user)}
                        >
                          <span
                            class="mode-name"
                            class:active={user.previlage === "Secretary"}
                            >Receiver</span
                          >
                        </li>
                      </Dropdown>
                    </div>
                  </div>
                </div>
              {/if}
            {/each}
          {/if}
        </div>
      </div>
    </div>
  {:else}
    There's no user yet!
  {/if}
</main>

<style>
  div.details-wrapper {
    position: fixed;
    inset: 0;
    z-index: 5;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    row-gap: 1rem;

    & div.arrow-wrapper {
      max-width: 50rem;
      width: 100%;
    }

    & div.details {
      padding: 0.5rem;
      background-color: var(--background);
      max-width: 50rem;
      width: 100%;
      border-radius: 2.5rem;
      display: flex;

      & img {
        max-width: 20rem;
        min-width: 15rem;
        border-radius: 2rem;
      }

      & div.credentials {
        width: 100%;
        padding: 0 0.5rem;

        & h1 {
          color: var(--main-col-3);
          font-size: 1.5rem;
          font-weight: 900;
          margin: 0.5rem 0;
        }

        & div.credential {
          border-bottom: 1px solid var(--header-color);
          display: flex;
          align-items: center;
          justify-content: space-between;
          color: var(--scroll-color);

          & p {
            font-weight: 600;
          }
        }

        & div.button-wrapper {
          display: flex;
          column-gap: 0.5rem;

          & button {
            transition: all ease-in-out 300ms;
            border: none;
            padding: 0.2rem 0;
            border-radius: 0.5rem;
            cursor: pointer;
            background-color: var(--component-active);
            position: relative;
          }

          & button:hover {
            background-color: var(--border-color);
            box-shadow: 5px 5px 25px rgba(0, 0, 0, 0.2);
          }

          & button::after {
            content: attr(data-content);
            position: absolute;
            top: -0.5rem;
            right: -0.5rem;
          }
        }

        & div.button-wrapper > * {
          flex: 1;
        }
      }
    }
  }

  main {
    max-width: 1300px;
    margin: auto;

    & div.search-sort-wrapper {
      display: flex;
      justify-content: space-between;
      margin: 0.5rem 0;
      position: relative;

      & input {
        border: 1px solid var(--header-color);
        border-radius: 3rem;
        background-color: transparent;
        padding: 0 1rem;
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

    & div.table-wrapper {
      & div.table {
        transition: all ease-in-out 500ms;

        & div.table-head {
          display: flex;
          transition: hover ease-in-out 500ms;

          & div.row {
            transition: all ease-in-out 500ms;
            flex: 1;
            font-weight: 700;
            padding: 1rem 0.5rem;
            border-left: 1px solid var(--main-col-6);
            color: var(--main-col-3);
            border-top: 1px solid var(--main-col-6);
            border-bottom: 1px solid var(--main-col-6);
          }

          & div.previlage {
            border-right: 1px solid var(--main-col-6);
          }

          & div.full-name {
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
          height: 35rem;
          overflow-y: auto;

          & div.table-body {
            margin: 0.3rem 0;
            display: flex;

            & div.user-cre-row {
              display: flex;
              flex: 6.5;
              transition: all ease-in-out 500ms;

              & div.row-cre {
                transition: all ease-in-out 300ms;
                padding: 0.7rem 0.5rem;
                white-space: nowrap;
                overflow: hidden;
                cursor: pointer;
                -webkit-mask: linear-gradient(90deg, white 50%, transparent);
                mask: linear-gradient(90deg, white 50%, transparent);
                flex: 1;
                position: relative;

                & img {
                  max-width: 3rem;
                  position: absolute;
                  top: 0;
                  left: 0;
                }
              }

              & div.user-name {
                flex: 2;

                & span.wrapper {
                  margin-left: 3rem;
                }
              }

              & div.dark {
                color: var(--main-col-2);
              }

              & div.name {
                border-left: none;
              }
            }

            & div.user-cre-row:hover {
              background-color: var(--header-color);
            }

            & div.user-cre-row.dark:hover {
              background-color: var(--navigation-hover-dark);
            }

            & div.action-wrapper {
              flex: 1;
              display: flex;
              align-items: center;
              justify-content: center;

              & div.action {
                display: flex;
                align-items: flex-end;
                margin-bottom: 0.2rem;
                column-gap: 0.3rem;
                cursor: pointer;
                padding: 0.2rem 0.5rem;
                border-radius: 0.3rem;
                transition: all ease-in-out 500ms;
                background-color: var(--component-active);
                color: var(--main-col-3);
                position: relative;

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
          }

          & div.table-body:nth-child(even) {
            background-color: var(--main-col-5);
          }

          & div.table-body.dark:nth-child(even) {
            background-color: var(--dark-main-col-6);
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
</style>
