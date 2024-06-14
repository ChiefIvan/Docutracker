<script lang="ts">
  import {
    dark,
    activeTab,
    handleDetails,
    type Users,
    userData,
  } from "../../store";
  import { tooltip } from "../shared/Tooltip";
  import { afterUpdate } from "svelte";
  import { fade } from "svelte/transition";
  import { flip } from "svelte/animate";

  export let filteredArray: Users[] = [];

  let approvedDocuments: Users[] = [];
  // let rejectedDocuments: Users[] = [];
  // let waitingDocuments: Users[] = [];

  const lastRoutes = ["OP", "Academic VP"];

  filteredArray.map((user) => {
    const approvedDocs = user.documents.filter((document) => {
      return (
        (document.documentPath.length &&
          document.documentPath[document.documentPath.length - 1].name ===
            $userData.unit &&
          document.documentPath[document.documentPath.length - 1].approved &&
          !document.documentPath[document.documentPath.length - 1].confirmed) ||
        (document.documentPath.length &&
          lastRoutes.includes(
            document.documentPath[document.documentPath.length - 1].name
          ) &&
          document.documentPath[document.documentPath.length - 1].confirmed &&
          !document.documentPath[document.documentPath.length - 1].finished &&
          !document.documentPath[document.documentPath.length - 1].complete) ||
        (document.documentPath.length &&
          lastRoutes.includes(
            document.documentPath[document.documentPath.length - 1].name
          ) &&
          document.documentPath[document.documentPath.length - 1].confirmed &&
          document.documentPath[document.documentPath.length - 1].finished &&
          !document.documentPath[document.documentPath.length - 1].complete)
      );
    });

    if (approvedDocs.length > 0) {
      approvedDocuments = [
        ...approvedDocuments,
        { ...user, documents: approvedDocs },
      ];
    }
  });

  // filteredArray.map((user) => {
  //   const rejectedDocs = user.documents.filter((document) => {
  //     return (
  //       document.documentPath.length &&
  //       document.documentPath[document.documentPath.length - 1].name ===
  //         route &&
  //       !document.documentPath[document.documentPath.length - 1].approved
  //     );
  //   });

  //   if (rejectedDocs.length > 0) {
  //     rejectedDocuments = [
  //       ...rejectedDocuments,
  //       { ...user, documents: rejectedDocs },
  //     ];
  //   }
  // });

  // filteredArray.map((user) => {
  //   const waitingDocs = user.documents.filter((document) => {
  //     return (
  //       document.documentPath.length &&
  //       document.documentPath[document.documentPath.length - 1].name ===
  //         route &&
  //       document.documentPath[document.documentPath.length - 1].approved &&
  //       document.documentPath[document.documentPath.length - 1].finished
  //     );
  //   });

  //   if (waitingDocs.length > 0) {
  //     waitingDocuments = [
  //       ...waitingDocuments,
  //       { ...user, documents: waitingDocs },
  //     ];
  //   }
  // });

  $: console.log(approvedDocuments);

  // $: console.log(rejectedDocuments);

  //   afterUpdate(() => {
  //     approvedArrayOr = $documents.filter(
  //       (document) =>
  //         document.documentPath.length &&
  //         document.documentPath.some((path) => path.approved && !path.confirmed)
  //     );

  //   });

  //   $: approvedArray = sortArray(
  //     searchArray(approvedArrayOr, searchValue),
  //     sortName
  //   );

  let statusNavigation = "Forwarded";

  // $: if ($activeTab === "Approved") {
  //   filteredArray = approvedDocuments;
  // } else if ($activeTab === "Rejected") {
  //   filteredArray = rejectedDocuments;
  // } else if ($activeTab === "Waiting") {
  //   filteredArray = waitingDocuments;
  // }
</script>

<!-- <div> -->
<section class="content-wrapper">
  {#if approvedDocuments.length}
    <div class="table-wrapper">
      <div class="table" class:dark={$dark}>
        <div class="table-head" class:dark={$dark}>
          <div class="designation" class:dark={$dark}>Author</div>
          <div class="name" class:dark={$dark}>Document Name</div>
          <div class="description" class:dark={$dark}>Document Description</div>
          <div class:dark={$dark}>Document ID</div>
          {#if $activeTab === "Approved"}
            <div class:dark={$dark}>Date</div>
          {:else}
            <div class:dark={$dark}>Approved Date</div>
          {/if}
        </div>
        <div class="body-wrapper">
          <!-- {#each [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] as count (count)}
              <div
                class="table-body"
                class:dark={$dark}
                use:tooltip={{
                  content: "Click for full details",
                  animation: "perspective-subtle",
                  theme: "tooltip",
                  arrow: true,
                  offset: [0, 15],
                }}
              >
                <div class="name" class:dark={$dark}>Sample</div>
                <div class="description" class:dark={$dark} title={"Sample"}>
                  Sample
                </div>
                <div class="id" class:dark={$dark}>Sample</div>
                <div class="date" class:dark={$dark}>Sample</div>
              </div>
            {/each} -->
          {#each approvedDocuments as filteredUser, i (i)}
            {#each filteredUser.documents as document (document.documentID)}
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <!-- svelte-ignore a11y-no-static-element-interactions -->
              <div
                class="table-body"
                class:dark={$dark}
                use:tooltip={{
                  content: "Click for full details",
                  animation: "perspective-subtle",
                  theme: "tooltip",
                  arrow: true,
                  offset: [0, 15],
                }}
                transition:fade
                animate:flip={{ duration: 500 }}
                on:click={() =>
                  handleDetails(
                    filteredUser.user_name,
                    filteredUser.email,
                    filteredUser.designation,
                    document,
                    "tab1"
                  )}
              >
                <div
                  class="user-name"
                  class:dark={$dark}
                  title={filteredUser.user_name}
                >
                  <img src={filteredUser.userImg} alt="Author Image" />
                  <span class="wrapper">{filteredUser.fullName}</span>
                </div>
                <div
                  class="doc-name"
                  class:dark={$dark}
                  title={document.documentName}
                >
                  {document.documentName}
                </div>
                <div
                  class="description"
                  class:dark={$dark}
                  title={document.documentDescription}
                >
                  {document.documentDescription}
                </div>
                <div class="id" class:dark={$dark} title={document.codeData}>
                  {document.codeData}
                </div>
                <div
                  class="date"
                  class:dark={$dark}
                  title={document.pendingDate}
                >
                  {document.pendingDate}
                </div>
              </div>
            {/each}
          {/each}
        </div>
      </div>
    </div>
  {:else}
    <h2 class="no-document" class:dark={$dark}>
      You don't have any Accepted Documents
    </h2>
  {/if}
</section>

<!-- </div> -->

<style>
  section.content-wrapper {
    & h2.no-document {
      line-height: 75vh;
      text-align: center;
      font-weight: bold;
      font-size: 3rem;
    }

    & h2.no-document.dark {
      color: var(--background);
    }

    & div.table-wrapper {
      & div.table {
        transition: all ease-in-out 500ms;

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

          & div.designation {
            border-left: none;
          }

          & div.name {
            /* border-left: none; */
          }

          & div.description {
            /* flex: 2; */
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
          max-height: 24.5rem;
          overflow-y: auto;

          & div.table-body {
            transition: all ease-in-out 500ms;
            display: flex;

            & div {
              transition: all ease-in-out 300ms;
              flex: 1;
              padding: 0.7rem 0.5rem;
              white-space: nowrap;
              overflow: hidden;
              cursor: pointer;
            }

            & div.dark {
              color: var(--main-col-2);
            }

            & div.user-name {
              display: flex;
              align-items: center;
              position: relative;
              /* padding-left: 5rem; */

              & img {
                border-radius: 50%;
                max-width: 2.5rem;
                position: absolute;
              }

              & span.wrapper {
                padding-left: 3rem;
              }
            }

            & div.name {
              /* flex: 2; */
              border-left: none;
            }

            & div.description {
              -webkit-mask: linear-gradient(90deg, white 50%, transparent);
              mask: linear-gradient(90deg, white 50%, transparent);
              /* flex: 2; */
            }

            & div.id {
              -webkit-mask: linear-gradient(90deg, white 50%, transparent);
              mask: linear-gradient(90deg, white 50%, transparent);
            }

            & div.date {
              -webkit-mask: linear-gradient(90deg, white 50%, transparent);
              mask: linear-gradient(90deg, white 50%, transparent);
            }
          }

          & div.table-body:nth-child(even) {
            background-color: var(--main-col-5);
          }

          & div.table-body.dark:nth-child(even) {
            background-color: var(--dark-main-col-6);
          }

          & div.table-body:hover {
            background-color: var(--header-color);
          }

          & div.table-body.dark:hover {
            background-color: var(--navigation-hover-dark);
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
