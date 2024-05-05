<script lang="ts">
  import {
    dark,
    documentSelected,
    documents,
    userData,
    detailsExpand,
    showMessage,
    registrationExpand,
  } from "../../store";
  import { createEventDispatcher } from "svelte";
  import { afterUpdate, onDestroy } from "svelte";

  import moment from "moment";
  import Card from "../shared/Card.svelte";
  import AddIcon from "../icons/AddIcon.svelte";
  import RequestIcon from "../icons/RequestIcon.svelte";
  import dashboard_banner from "../../assets/dashborad_banner.png";
  import TriangleIcon from "../icons/TriangleIcon.svelte";
  import Status from "./Status.svelte";
  import DocumentModal from "./DocumentModal.svelte";

  export let authToken = "";

  let dispatch = createEventDispatcher();

  let docN = "";
  let docid = "";
  let appDate = "";
  let comDate = "";

  $: selectedDocument = $documents.find((document) => {
    return document.codeData === docid;
  });

  afterUpdate(() => {
    docid = localStorage.getItem("docid") || "";

    let documentExistance = $documents.filter(
      (document) => document.documentName === localStorage.getItem("docN")
    );

    if (documentExistance.length) {
      docN = localStorage.getItem("docN") || "";
      docid = localStorage.getItem("docid") || "";
    }

    console.log(documentExistance);
  });

  let days = 0;
  let hours = 0;
  let minutes = 0;
  let seconds = 0;

  $: if (
    selectedDocument &&
    selectedDocument.documentPath &&
    selectedDocument.documentPath.length
  ) {
    comDate =
      selectedDocument.documentPath[selectedDocument.documentPath.length - 1]
        .completeDate || "";
    console.log(comDate);
    appDate = selectedDocument.documentPath[0].approvedDate || "";
  }

  $: if (appDate.length && comDate.length) {
    let approvedTime = moment(appDate, "ddd, DD MMM YYYY HH:mm:ss z");
    let completedTime = moment(comDate, "ddd, DD MMM YYYY HH:mm:ss z");
    let duration = moment.duration(completedTime.diff(approvedTime));

    days = duration.days();
    hours = duration.hours();
    minutes = duration.minutes();
    seconds = duration.seconds();
  } else {
    setInterval(() => {
      if (!comDate.length) {
        let currentTime = moment();
        let eventTime = moment(appDate, "ddd, DD MMM YYYY HH:mm:ss z");

        if (currentTime.isAfter(eventTime)) {
          let duration = moment.duration(currentTime.diff(eventTime));

          days = duration.days();
          hours = duration.hours();
          minutes = duration.minutes();
          seconds = duration.seconds();
        }
      }
    }, 1000);
  }

  const registerDocument = () => {
    if (!$userData.full_ver_val) {
      $showMessage = {
        error: "You must be a fully registered User! ^_^.",
      };
      $registrationExpand = true;
      return;
    }

    $documentSelected = "";

    let editData = {
      documentName: "",
      documentProgram: "",
      codeData: "",
      documentDes: "",
      isEdit: false,
    };

    dispatch("edit", editData);
    dispatch("switch", "Register Document");
  };

  let infoExpand = false;
  const handleInfoExpand = () => {
    infoExpand = !infoExpand;
  };

  let documentDesSelected = "";
  let documentCodeSelected = "";
  let documentProgramSelected = "";

  const handleDocumentEdit = (documentName: string, documentID: string) => {
    for (let document of $documents) {
      if (
        document.documentName === documentName &&
        documentID === document.codeData
      ) {
        documentCodeSelected = document.codeData;
        documentDesSelected = document.documentDescription;
        documentProgramSelected = document.documentProgram;
      }
    }

    let editData = {
      documentName: documentName,
      documentProgram: documentProgramSelected,
      codeData: documentCodeSelected,
      documentDes: documentDesSelected,
      isEdit: true,
    };

    dispatch("edit", editData);
    dispatch("switch", "Register Document");
  };

  $: check =
    selectedDocument &&
    selectedDocument.documentPath &&
    !selectedDocument.documentPath.length;

  const handleCheck = () => {
    if (check) {
      handleDocumentEdit(docN, docid);
    }
  };

  onDestroy(() => ($documentSelected = ""));
</script>

<svelte:head>
  <title>DOCUTRACKER | Dashboard</title>
</svelte:head>

{#if $detailsExpand}
  <DocumentModal {authToken}></DocumentModal>
{/if}

<main>
  <div class="shortcut-trackinfo">
    <div class="shortcut-wrapper">
      <h2 class:dark={$dark}>Shortcuts</h2>
      <div class="card-wrapper">
        <Card on:click={registerDocument}>
          <div class="svg-wrapper" class:dark={$dark}>
            <AddIcon></AddIcon>
          </div>
          <div class="label-wrapper">
            <p class:dark={$dark}>Add Document</p>
            <span class:dark={$dark}>Register or Add Documents</span>
          </div>
        </Card>
        <Card
          on:click={() => {
            $documentSelected = "";
            dispatch("switch", "Scan Document");
          }}
        >
          <div class="svg-wrapper" class:dark={$dark}>
            <RequestIcon></RequestIcon>
          </div>
          <div class="label-wrapper">
            <p class:dark={$dark}>Scan Document</p>
            <span class:dark={$dark}>Find your Documents</span>
          </div>
        </Card>
      </div>
    </div>
    <div
      class="tracking-info-wrapper"
      class:dark={$dark}
      class:isExpand={infoExpand}
    >
      <div class="tracking-wrapper" class:expanded={infoExpand}>
        {#if docN.length && docid.length}
          <div
            class="document-name-wrapper"
            style="display: flex; justify-content: space-evenly;"
          >
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <div
              class="name-wrap"
              style="display: flex; align-items: center; 
            margin-bottom: 2rem;
            "
            >
              <span
                class:uneditable={!check}
                class="document-name"
                class:dark={$dark}
                on:click={handleCheck}
              >
                {docN}
              </span>
              <TriangleIcon on:click={handleInfoExpand} rotate={infoExpand}
              ></TriangleIcon>
            </div>
            <span
              class:dark={$dark}
              style="font-size: 1.5rem;
            font-weight: bold;">{days}d {hours}h {minutes}m {seconds}s</span
            >
          </div>
          {#each $documents as value, i (i)}
            {#if value.codeData === docid}
              <!-- {@const lastPath =
              value.documentPath[value.documentPath.length - 1]} -->
              <!-- reverse Possible Problem -->
              {#each Array(value.documentPath.length) as _, i (i)}
                {@const pathValue =
                  value.documentPath[value.documentPath.length - 1 - i]}
                {#if pathValue.approved && pathValue.confirmed && pathValue.finished && pathValue.complete}
                  <div class="info-wrapper">
                    <div class="date-wrapper">
                      <p class:dark={$dark}>{pathValue.completeDate}</p>
                    </div>
                    <div class="info">
                      <h3 class:dark={$dark}>Status: Complete</h3>
                      <span class:dark={$dark}
                        >This Document is waiting to be passed on to the next
                        step in the process and ready to be approve by the
                        secretary of the next route. Please proceed to that
                        route as soon as possible.</span
                      >
                    </div>
                  </div>
                {/if}
                {#if pathValue.approved && pathValue.finished}
                  <div class="info-wrapper">
                    <div class="date-wrapper">
                      <p class:dark={$dark}>{pathValue.finishDate}</p>
                    </div>
                    <div class="info">
                      <h3 class:dark={$dark}>
                        Status: Waiting for the recipient
                      </h3>
                      <span class:dark={$dark}
                        >Your document is finished and is waiting for you to
                        claim from {pathValue.name}. Please get your document
                        immediately!</span
                      >
                    </div>
                  </div>
                  <div class="info-wrapper">
                    <div class="date-wrapper">
                      <p class:dark={$dark}>{pathValue.finishDate}</p>
                    </div>
                    <div class="info">
                      <h3 class:dark={$dark}>Status: Finished</h3>
                      <span class:dark={$dark}
                        >Your document has been processed successfully</span
                      >
                    </div>
                  </div>
                {/if}
                {#if pathValue.approved && pathValue.confirmed && !pathValue.finished}
                  <div class="info-wrapper">
                    <div class="date-wrapper">
                      <p class:dark={$dark}>{pathValue.confirmedDate}</p>
                    </div>
                    <div class="info">
                      <h3 class:dark={$dark}>Status: To be Forwarded</h3>
                      <span class:dark={$dark}
                        >This Document is waiting to be passed on to the next
                        step in the process and ready to be approve by the
                        reciever of the next route. Please proceed to that route
                        as soon as possible.</span
                      >
                    </div>
                  </div>
                  <div class="info-wrapper">
                    <div class="date-wrapper">
                      <p class:dark={$dark}>{pathValue.confirmedDate}</p>
                    </div>
                    <div class="info">
                      <h3 class:dark={$dark}>
                        Status: Confirmed by {pathValue.name}
                      </h3>
                      <span class:dark={$dark}
                        >Lorem ipsum dolor, sit amet consectetur adipisicing
                        elit. Distinctio ut suscipit eaque temporibus iste error
                        consequatur necessitatibus dolor repellat odio.</span
                      >
                    </div>
                  </div>
                {/if}
                {#if pathValue.approved && pathValue.processing}
                  <div class="info-wrapper">
                    <div class="date-wrapper">
                      <p class:dark={$dark}>{pathValue.approvedDate}</p>
                    </div>
                    <div class="info">
                      <h3 class:dark={$dark}>Status: Processing</h3>
                      <span class:dark={$dark}
                        >Your document is now under Processing, please wait for
                        several hours or days for the processing to complete.</span
                      >
                    </div>
                  </div>
                  <div class="info-wrapper">
                    <div class="date-wrapper">
                      <p class:dark={$dark}>{pathValue.approvedDate}</p>
                    </div>
                    <div class="info">
                      <h3 class:dark={$dark}>
                        Status: Approved by {pathValue.name}
                      </h3>
                      <span class:dark={$dark}
                        >Your document has arrived at the {pathValue.name} and document
                        has been approved, this signifies that the transaction is
                        successful.</span
                      >
                    </div>
                  </div>
                {/if}
                {#if !pathValue.approved}
                  <div class="info-wrapper">
                    <div class="date-wrapper">
                      <p class:dark={$dark}>{pathValue.disapprovedDate}</p>
                    </div>
                    <div class="info">
                      <h3 class:dark={$dark}>
                        Status: Unsuccessful {pathValue.name}
                      </h3>
                      <span class:dark={$dark}
                        >Your document has arrived at the {pathValue.name} but unfortunately,
                        the {pathValue.name} disapproved your document, this signifies
                        that the transaction is unsuccessful.</span
                      >
                    </div>
                  </div>
                {/if}
              {/each}
              {#if value.pending}
                <div class="info-wrapper">
                  <div class="date-wrapper">
                    <p class:dark={$dark}>{value.pendingDate}</p>
                  </div>
                  <div class="info">
                    <h3 class:dark={$dark}>
                      Status: To be Forwarded
                      <!-- {#if value.documentName === "Faculty Loading"}
                      Program Head
                    {/if} -->
                    </h3>
                    <span class:dark={$dark}
                      >This Document is waiting to be passed on to the next step
                      in the process and ready to be approve by the reciever of
                      the first route. Please proceed to that route as soon as
                      possible.</span
                    >
                  </div>
                </div>
              {/if}
            {/if}
          {/each}
        {:else}
          <p class="not-selected" class:dark={$dark}>
            Search for Document first!
          </p>
          <div class="image-wrapper">
            <img src={dashboard_banner} alt="Dashboard Banner" />
          </div>
        {/if}
      </div>
      <!-- {#if docN.length && docid.length}
        <div class="counter-wrapper">
          <span class="counter-label" class:dark={$dark}>
            {#if comDate}
              Total
            {/if}
            Processing Time</span
          >
          <span class="counter" class:dark={$dark}
            ></span
          >
        </div>
      {/if} -->
    </div>
  </div>
  <!-- <div class="button-wrapper">
    <Button on:click={() => print()}>Generate Tracking Report</Button>
  </div> -->
  <Status></Status>
</main>

<style>
  main {
    & div.shortcut-trackinfo {
      display: flex;
      /* background-color: var(--border-color); */

      & div.tracking-info-wrapper {
        flex: 1;
        -webkit-mask: linear-gradient(white 20%, transparent);
        mask: linear-gradient(white 20%, transparent);
        overflow: hidden;
        position: relative;
        padding: 0 4rem;
        padding-top: 2rem;
        transition: all ease-in-out 800ms;
        display: grid;
        grid-template-rows: 0fr;

        & div.tracking-wrapper {
          padding-bottom: 10rem;
          min-height: 50vh;
          max-height: 80vh;
          max-width: 40rem;
          text-align: center;
          width: 100%;

          & span.document-name {
            font-size: 1.5rem;
            font-weight: bold;
            display: inline-block;
            margin-right: 0.5rem;
            cursor: pointer;
            position: relative;
          }

          & span.document-name:hover::after {
            content: "Click to Edit";
            white-space: nowrap;
            position: absolute;
            width: auto;
            top: 0;
            right: -9rem;
            transform: translateY(20%);
            background-color: var(--main-col-3);
            color: var(--background);
            padding: 0.3rem 0.5rem;
          }

          & span.uneditable:hover::after {
            display: none;
          }

          & span.uneditable {
            cursor: default;
          }

          & span {
            transition: all ease-in-out 300ms;
            color: var(--scroll-color);
          }

          & span.dark {
            color: var(--background);
          }

          & div.info-wrapper {
            display: flex;
            text-align: start;

            & div.date-wrapper {
              width: 10rem;
              padding-right: 1rem;

              & p {
                transition: all ease-in-out 300ms;
                color: var(--scroll-color);
              }

              & p.dark {
                color: var(--main-col-7);
              }
            }

            & div.info {
              position: relative;
              border-left: 1px solid var(--scroll-color);
              width: 30rem;
              padding: 0 2rem;

              & h3 {
                transition: all ease-in-out 300ms;
                font-size: 1.1rem;
                font-weight: bold;
                margin-bottom: 1rem;
              }

              & h3.dark {
                color: var(--background);
              }

              & span {
                display: inline-block;
                padding-bottom: 3rem;
                color: var(--scroll-color);
                transition: all ease-in-out 300ms;
              }

              & span.dark {
                color: var(--main-col-2);
              }
            }

            & div.info::after {
              content: "";
              height: 1.6rem;
              width: 1.6rem;
              border-radius: 50%;
              background-color: var(--dark-main-col-1);
              position: absolute;
              top: 0;
              left: -0.8rem;
            }
          }

          & div.image-wrapper {
            /* width: 85%; */
            /* position: absolute; */
            text-align: center;
            bottom: -5rem;
            z-index: 1;

            & img {
              max-width: 25rem;
            }
          }

          & p.not-selected {
            transition: all ease-in-out 300ms;
            color: var(--main-col-3);
            font-size: 1.5rem;
            font-weight: 900;
            margin-left: 1.5rem;
          }

          & p.dark {
            color: var(--background);
          }
        }

        & div.counter-wrapper {
          position: absolute;
          top: 0;
          bottom: 0;
          right: 10%;
          display: flex;
          align-items: flex-start;
          justify-content: center;
          flex-direction: column;

          & span.counter-label {
            font-weight: bold;
            font-size: 1.1rem;
            transition: all ease-in-out 300ms;
          }

          & span.counter-label.dark {
            color: var(--background);
          }

          & span.counter {
            transition: all ease-in-out 300ms;
            font-weight: bold;
            font-size: 3rem;
          }

          & span.counter.dark {
            color: var(--main-col-7);
          }
        }

        & div.tracking-wrapper::-webkit-scrollbar {
          width: 0.5rem;
          height: 0.5rem;
        }

        & div.tracking-wrapper::-webkit-scrollbar-track {
          background: var(--main-col-6);
        }

        & div.tracking-wrapper::-webkit-scrollbar-thumb {
          background: var(--main-col-3);
        }

        & div.tracking-wrapper::-webkit-scrollbar-thumb:hover {
          background: var(--scroll-color);
        }

        & div.expanded {
          overflow-y: auto;
        }
      }

      & div.shortcut-wrapper {
        padding: 0 4rem;
        padding-top: 2rem;
        flex: 1;

        & h2 {
          font-size: 1.5rem;
          font-weight: 900;
          color: var(--scroll-color);
          /* margin-top: 1rem; */
          margin-bottom: 1rem;
          transition: all ease-int-out 300ms;
        }

        & h2.dark {
          color: var(--background);
        }

        & div.card-wrapper {
          display: flex;
          justify-content: center;
          column-gap: 2rem;
          row-gap: 1rem;
          margin-bottom: 1rem;

          & div.svg-wrapper {
            height: 70%;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: var(--border-color);
            transition: all ease-int-out 300ms;
          }

          & div.svg-wrapper.dark {
            background-color: var(--dark-main-col-1);
          }

          & p {
            font-weight: 700;
            font-size: 1rem;
            color: var(--scroll-color);
            transition: all ease-in-out 300ms;
          }

          & p.dark {
            color: var(--icon-dark);
          }

          & span {
            color: var(--scroll-color);
            transition: all ease-int-out 300ms;
          }

          & span.dark {
            color: var(--icon-dark);
          }
        }

        & div.label-wrapper {
          margin-top: 1rem;
          margin-left: 1rem;
        }
      }
    }

    & div.isExpand {
      grid-template-rows: 1fr;
    }

    & div.tracking-info-wrapper.dark {
      /* background-color: var(--dark-main-col-6); */
    }

    & div.button-wrapper {
      margin: auto;
      max-width: 50rem;
    }
  }

  @media (max-width: 750px) {
    main div.shortcut-wrapper div.card-wrapper {
      flex-direction: column;
    }
  }
</style>
