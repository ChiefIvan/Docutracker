<script lang="ts">
  import {
    dark,
    handleFetch,
    address,
    showMessage,
    selectExpand,
    selectProgramExpand,
    selectInstituteExpand,
    selectDeanInstituteExpand,
    selectRouteExpand,
    modeExpand,
    userData,
    documents,
    type RequestAPI,
    type ResponseData,
  } from "../../store";
  import { v4 as uuidv4 } from "uuid";
  import { fade } from "svelte/transition";
  import { tooltip } from "../shared/Tooltip";
  import { createEventDispatcher, onDestroy, onMount } from "svelte";

  import QrCode from "svelte-qrcode";
  import Button from "../shared/Button.svelte";
  import TriangleIcon from "../icons/TriangleIcon.svelte";
  import MediaQuery from "../shared/MediaQuery.svelte";
  import Dropdown from "../shared/Dropdown.svelte";
  import Input from "../shared/Input.svelte";

  let placeholderHovered = false;
  let qrCodeElement: any;
  let dispatch = createEventDispatcher();

  export let authToken = "";
  export let editData: any;

  const date = new Date().toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  let value = "";

  const handleGenerate = () => {
    if (value.length) {
      return;
    }

    if (!documentSelected.length) {
      $showMessage = { error: "Please Select a Document first!" };
      return;
    }

    if (!documentDescription.length) {
      $showMessage = { error: "Please Provide a Description first!" };
      return;
    }

    value = uuidv4();
  };

  let download = false;

  const handleDownload = () => {
    let imgElement = qrCodeElement.querySelector("img.qrcode");
    let base64Image = imgElement.src;

    const downloadLink = document.createElement("a");
    downloadLink.href = base64Image;
    downloadLink.download = `${documentSelected}.png`;
    downloadLink.click();

    download = true;
  };

  let documentDescription = "";
  let programSelected = "";
  let documentSelected = "";
  let instituteSelected = "";
  let edit = false;

  onMount(() => {
    if (editData && Object.keys(editData).length !== 0) {
      const {
        documentName,
        documentProgram,
        codeData,
        documentDes,
        isEdit,
        documentInstitute,
        deanInstitute,
      } = editData;

      documentSelected = documentName;
      programSelected = documentProgram;
      instituteSelected = documentInstitute;
      documentDescription = documentDes;
      value = codeData;
      edit = isEdit;
    }
  });

  const registrationMethod = "POST";
  const registrationAddress = `${address}/document_register`;
  const registrationRequest: RequestAPI = {
    method: registrationMethod,
    address: registrationAddress,
    credentials: {
      codeData: "",
      documentName: "",
      documentProgram: "",
      documentInstitute: "",
      deanInstitute: "",
      documentDescription: "",
      edit: false,
    },
  };

  const instituteSelection = ["FALS", "FCDSET", "FGBM", "FNAHS", "FTED"];
  const programSelection = {
    FALS: ["BSB", "BSA", "BSES", "BSAM", "BSDC"],
    FCDSET: ["BSCE", "BSM", "BITM", "BSIT"],
    FGBM: ["BSC", "BSBA", "BSHM"],
    FNAHS: ["BSN"],
    FTED: ["BEE", "BECE", "BSNE", "BTLE"],
  };

  const handleSubmit = async () => {
    if ($userData.institute === "FALS") {
      registrationRequest.credentials!.deanInstitute = "FALS";
    }

    if ($userData.institute === "FCDSET") {
      registrationRequest.credentials!.deanInstitute = "FCDSET";
    }

    if ($userData.institute === "FGBM") {
      registrationRequest.credentials!.deanInstitute = "FGBM";
    }

    if ($userData.institute === "FNAHS") {
      registrationRequest.credentials!.deanInstitute = "FNAHS";
    }

    if ($userData.institute === "FTED") {
      registrationRequest.credentials!.deanInstitute = "FTED";
    }

    registrationRequest.credentials!.codeData = value;
    registrationRequest.credentials!.documentName = documentSelected;
    registrationRequest.credentials!.documentInstitute = instituteSelected;
    registrationRequest.credentials!.documentName = documentSelected;
    registrationRequest.credentials!.documentProgram = programSelected;
    registrationRequest.credentials!.documentDescription = documentDescription;
    registrationRequest.credentials!.edit = edit;

    if (!documentSelected.length) {
      $showMessage = { error: "Please Select a Document first!" };
      return;
    }

    if (!customDocumentname.length) {
      if (!instituteSelected.length) {
        if (!["Program Head", "Dean Office"].includes($userData.unit)) {
          $showMessage = {
            error: "Please Select proper Institue of the Program Head first!",
          };
          return;
        }
      }

      if (!["Program Head", "Dean Office"].includes($userData.unit)) {
        if (!programSelected.length) {
          $showMessage = { error: "Please Select a Program first!" };
          return;
        }
      }
    }

    if (!documentDescription.length) {
      $showMessage = { error: "Please Provide a Document Desciption!" };
      return;
    }

    if (!value.length) {
      $showMessage = { error: "Please Generate a Code first!" };
      return;
    }

    if (!edit) {
      if (!download) {
        $showMessage = { error: "Please download your QR Image first!" };
        return;
      }
    }

    const request: ResponseData = await handleFetch(
      registrationRequest,
      authToken
    );

    if (request.error) {
      $showMessage = request;
    } else {
      if (edit) {
        location.reload();
      } else {
        $showMessage = {
          success: `You Registered ${documentSelected} successfully. Go to dashboard to see its status.`,
        };

        localStorage.setItem("docN", documentSelected);
        localStorage.setItem("docid", value);
      }

      download = false;

      const date = new Date();
      documents.update((docs) => [
        ...docs,
        {
          pending: true,
          documentID: Math.random(),
          codeData: value,
          attemps: 0,
          documentName: documentSelected,
          documentDescription: documentDescription,
          pendingDate: date.toISOString(),
          documentPath: [],
        },
      ]);

      (document.activeElement as HTMLElement).blur();
      documentSelected = "";
      instituteSelected = "";
      programSelected = "";
      documentDescription = "";
      value = "";
    }
  };

  const handleExpand = () => {
    $selectExpand = !$selectExpand;
    $modeExpand = false;
  };

  const handleInstituteExpand = () => {
    $selectDeanInstituteExpand = false;
    $selectInstituteExpand = !$selectInstituteExpand;
    $modeExpand = false;
  };

  const handleDeanInstituteExpand = () => {
    $selectInstituteExpand = false;
    $selectDeanInstituteExpand = !$selectDeanInstituteExpand;
    $modeExpand = false;
  };

  const handleProgramExpand = () => {
    $selectProgramExpand = !$selectProgramExpand;
    $modeExpand = false;
  };

  const handleClose = () => {
    dispatch("switch");
  };

  onDestroy(() => {
    download = false;
  });

  const documentsSelection = [
    {
      id: 1,
      name: "Faculty Loading",
    },
    {
      id: 2,
      name: "Requested Subject",
    },
    {
      id: 3,
      name: "Endorsement Form",
    },
    {
      id: 4,
      name: "Others: Please Specify!",
    },
  ];

  let openRoutes = false;

  let selectedID = 0;
  let openOther = false;

  $: if (selectedID === 4) {
    openOther = !openOther;
  }

  let customDocumentname = "";
  let routeSelected = "";
  let selectedRoutes = [];

  const routeSelection = [
    { id: 0, name: "Secretary" },
    { id: 1, name: "Program Head" },
    { id: 2, name: "Dean Office" },
    { id: 3, name: "Academic VP" },
    { id: 4, name: "OP" },
  ];

  const handleCustomSubmit = () => {
    documentSelected = customDocumentname;
  };
</script>

{#if openRoutes}
  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div
    class="overlay"
    transition:fade
    on:click|self={() => (openRoutes = !openRoutes)}
  >
    <div class="select-route" class:dark={$dark}>
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-static-element-interactions -->
      {#if !["Program Head", "Dean Office"].includes($userData.unit)}
        <h1 class:dark={$dark} class="unit-name">Program Head</h1>
        <div class="program-head">
          <div
            class="selected-wrapper"
            on:click|stopPropagation={handleInstituteExpand}
            transition:fade
          >
            <div
              class="selected"
              use:tooltip={{
                content:
                  "One of routes of this document is Program Head, you must select what institute of the Program Head that recieves this document",
                animation: "perspective-subtle",
                theme: "tooltip",
                offset: [0, 0],
                placement: "bottom",
              }}
              class:dark={$dark}
            >
              <p class:dark={$dark}>
                {#if instituteSelected && instituteSelected.length !== 0}
                  {instituteSelected}
                {:else}
                  Please select an Institute
                {/if}
              </p>
              <TriangleIcon rotate={$selectInstituteExpand}></TriangleIcon>
            </div>
            <Dropdown expand={$selectInstituteExpand} docs={true}>
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
              {#each instituteSelection as value, i (i)}
                <li
                  class="list-wrapper"
                  class:active={value === instituteSelected}
                  class:dark={$dark}
                  on:click={() => {
                    instituteSelected = value;
                    programSelected = "";
                  }}
                >
                  <span
                    class="document-name"
                    class:dark={$dark}
                    class:active={value === instituteSelected}>{value}</span
                  >
                </li>
              {/each}
            </Dropdown>
          </div>
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          {#if instituteSelected && instituteSelected.length !== 0}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div
              class="selected-wrapper"
              on:click|stopPropagation={handleProgramExpand}
              transition:fade
            >
              <div
                class="selected"
                use:tooltip={{
                  content:
                    "You must also select what program of the Program Head that recieves this document",
                  animation: "perspective-subtle",
                  theme: "tooltip",
                  offset: [0, 0],
                  placement: "bottom",
                }}
                class:dark={$dark}
              >
                <p class:dark={$dark}>
                  {#if programSelected && programSelected.length !== 0}
                    {programSelected}
                  {:else}
                    Please select a Program
                  {/if}
                </p>
                <TriangleIcon rotate={$selectProgramExpand}></TriangleIcon>
              </div>
              <Dropdown expand={$selectProgramExpand} docs={true}>
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
                {#each programSelection[instituteSelected] as value, i (i)}
                  <li
                    class="list-wrapper"
                    class:active={value === programSelected}
                    class:dark={$dark}
                    on:click={() => (programSelected = value)}
                  >
                    <span
                      class="document-name"
                      class:dark={$dark}
                      class:active={value === programSelected}>{value}</span
                    >
                  </li>
                {/each}
              </Dropdown>
            </div>
          {/if}
        </div>
      {/if}
    </div>
  </div>
{/if}

{#if openOther}
  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="overlay">
    <div class="main-wrapper">
      <div class="custom-document-wrapper">
        <Input
          overlap
          inputName="Document Name"
          inputType="text"
          on:input={(e) => (customDocumentname = e.target.value)}
        ></Input>
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div
          class="selected-wrapper"
          on:click|stopPropagation={() =>
            ($selectRouteExpand = !$selectRouteExpand)}
          transition:fade
        >
          <div class="selected">
            <p class:dark={$dark}>
              {#if routeSelected && routeSelected.length !== 0}
                {routeSelected}
              {:else}
                Please select Routes
              {/if}
            </p>
            <Dropdown customRoute={true} expand={$selectRouteExpand}>
              {#each routeSelection as route (route.id)}
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
                <li
                  class="list-wrapper"
                  class:active={route.name === routeSelected}
                  class:dark={$dark}
                  on:click={() => {
                    if (customDocumentname.length) {
                      selectedRoutes = [
                        ...selectedRoutes,
                        {
                          id: route.id,
                          name: route.name,
                          institute: "",
                          program: "",
                        },
                      ];
                    } else {
                      $showMessage = {
                        error: "Please Write the name of the Document first!",
                      };
                    }
                  }}
                >
                  <span
                    class="document-name"
                    class:dark={$dark}
                    class:active={route.name === routeSelected}
                    >{route.name}</span
                  >
                </li>
              {/each}
            </Dropdown>
          </div>
        </div>
        <div class="button-wrapper">
          <Button
            on:click={() => {
              selectedID = 0;
              openOther = false;
              documentSelected = "";
              selectedRoutes = [];
              customDocumentname = "";
            }}>Go Back</Button
          >
          <Button
            on:click={() => {
              selectedID = 0;
              handleCustomSubmit();
              openOther = false;
            }}>Submit</Button
          >
        </div>
      </div>
      {#if customDocumentname.length}
        <div class="summary-wrapper" transition:fade>
          <h1>Summary</h1>
          <h2>{customDocumentname}</h2>
          <div class="selected-route-wrapper">
            <h1>Route Selected</h1>
            {#each selectedRoutes as route (route.id)}
              <p
                use:tooltip={{
                  content: "Click to Remove",
                  animation: "perspective-subtle",
                  theme: "tooltip",
                }}
              >
                {route.name}
              </p>
            {/each}
          </div>
        </div>
      {/if}
    </div>
  </div>
{/if}

<div class="register-document-wrapper">
  <form
    class="register-document-form"
    on:submit|preventDefault
    autocomplete="off"
  >
    <div class="credential-wrapper">
      <h2 class="unit-title">{$userData.unit}'s Documents</h2>
      <span class="date" class:dark={$dark}
        >Author/Owner: {$userData.fullName}
      </span>
      <!-- svelte-ignore missing-declaration -->
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-static-element-interactions -->
      <div class="select-wrapper">
        <div class="selected-wrapper" on:click|stopPropagation={handleExpand}>
          <div class="selected" class:dark={$dark}>
            <p class:dark={$dark}>
              {#if documentSelected.length !== 0}
                {documentSelected}
              {:else}
                Please select a document
              {/if}
            </p>
            <TriangleIcon rotate={$selectExpand}></TriangleIcon>
          </div>
          <Dropdown expand={$selectExpand} docs={true}>
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
            {#each documentsSelection as value (value.id)}
              <li
                class="list-wrapper"
                class:active={value.name === documentSelected}
                class:dark={$dark}
                on:click={() => {
                  programSelected = "";
                  instituteSelected = "";
                  documentSelected = value.name;
                  selectedID = value.id;
                }}
              >
                <span
                  class="document-name"
                  class:dark={$dark}
                  class:active={value.name === documentSelected}
                  >{value.name}</span
                >
              </li>
            {/each}
          </Dropdown>
          {#if documentSelected === "Faculty Loading"}
            <p class="routes" class:dark={$dark}>
              {#if $userData.unit === "Program Head"}
                Route: Dean Office / Academic VP
              {:else if $userData.unit === "Dean Office"}
                Route: Academic VP
              {:else}
                Route: Program Head / Dean Office / Academic VP
              {/if}
            </p>
          {:else if documentSelected === "Requested Subject"}
            <p class="routes" class:dark={$dark}>
              {#if $userData.unit === "Program Head"}
                Route: Dean Office / Academic VP
              {:else if $userData.unit === "Dean Office"}
                Route: Academic VP
              {:else}
                Route: Program Head / Dean Office / Academic VP
              {/if}
            </p>
          {:else if documentSelected === "Endorsement Form"}
            <p class="routes" class:dark={$dark}>
              {#if $userData.unit === "Program Head"}
                Route: Dean Office / Academic VP / OP
              {:else if $userData.unit === "Dean Office"}
                Route: Academic VP / OP
              {:else}
                Route: Program Head / Dean Office / Academic VP
              {/if}
            </p>
          {:else if customDocumentname.length}
            <p class="routes" class:dark={$dark}>
              Route:
              {#each selectedRoutes as route, i (i)}
                {route.name} /
              {/each}
            </p>
          {/if}
        </div>
        {#if $userData.unit !== "Program Head"}
          {#if documentSelected.length && selectedID !== 4}
            <Button
              on:click={() => {
                openRoutes = !openRoutes;
              }}>Specify Route</Button
            >
          {/if}
        {/if}
      </div>

      <textarea
        class:dark={$dark}
        placeholder="Document Description (Mandatory)"
        bind:value={documentDescription}
      ></textarea>
      <MediaQuery query="(max-width: 900px)" let:matches>
        {#if matches}
          <div class="code-wrapper">
            <!-- svelte-ignore missing-declaration -->
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <div
              class="code-placeholder"
              class:dark={$dark}
              bind:this={qrCodeElement}
              on:click|stopPropagation={handleGenerate}
              on:mouseenter={() => {
                placeholderHovered = true;
              }}
              on:mouseleave={() => {
                placeholderHovered = false;
              }}
            >
              {#if value && value.length}
                <QrCode {value}></QrCode>
                {#if value && value.length && placeholderHovered}
                  <div
                    transition:fade
                    class="code-overlap"
                    on:click={handleDownload}
                  >
                    <span class="download-qr">Download Image</span>
                  </div>
                {/if}
              {:else}
                <span class="qr-label">Generate QR Code</span>
              {/if}
            </div>
          </div>
        {/if}
      </MediaQuery>
      <div class="button-wrapper">
        <div class="button">
          <Button hoverized={true} on:click={handleClose}>Go Back</Button>
          {#if edit}
            <Button
              on:click={handleSubmit}
              disabled={!value.length}
              hoverized={true}>Save</Button
            >
          {:else}
            <Button
              on:click={handleSubmit}
              disabled={!value.length}
              hoverized={true}>Submit</Button
            >
          {/if}
        </div>
      </div>
    </div>
    <MediaQuery query="(min-width: 900px)" let:matches>
      {#if matches}
        <div class="code-wrapper">
          <span class="date" class:dark={$dark}>{date}</span>
          <!-- {#if documentSelected.length}
            <div
              transition:fade
              class="
          code-placeholder
          route-wrapper"
              class:dark={$dark}
            >
              Hello
            </div>
          {/if} -->
          <!-- svelte-ignore missing-declaration -->
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <div
            class="code-placeholder"
            class:dark={$dark}
            bind:this={qrCodeElement}
            on:click|stopPropagation={handleGenerate}
            on:mouseenter={() => {
              placeholderHovered = true;
            }}
            on:mouseleave={() => {
              placeholderHovered = false;
            }}
          >
            {#if value && value.length}
              <QrCode {value}></QrCode>
              {#if value && value.length && placeholderHovered}
                <div
                  transition:fade
                  class="code-overlap"
                  on:click={handleDownload}
                >
                  <span class="download-qr">Download Image</span>
                </div>
              {/if}
            {:else}
              <span class="qr-label">Generate QR Code</span>
            {/if}
          </div>
        </div>
      {/if}
    </MediaQuery>
  </form>
</div>

<style>
  h2.unit-title {
    font-size: 1.5rem;
    font-weight: 900;
    color: var(--scroll-color);
  }

  h1.unit-name {
    font-size: 1rem;
    color: var(--input-color);
    margin-bottom: 0.5rem;
  }

  h1.unit-name.dark {
    color: var(--header-color);
  }

  div.overlay {
    position: fixed;
    inset: 0;
    display: grid;
    place-items: center;
    z-index: 5;
    background-color: rgba(0, 0, 0, 0.6);

    & div.main-wrapper {
      display: flex;
      align-items: center;
      justify-content: center;
      column-gap: 1rem;

      & div.custom-document-wrapper {
        background-color: #fff;
        padding: 1rem;
        border-radius: 0.5rem;
        max-width: 500px;
        width: 100%;

        & div.selected-wrapper {
          position: relative;
          margin-bottom: 1rem;
          width: 100%;

          & div.selected {
            transition: all ease-in-out 300ms;
            border: 1px solid var(--header-color);
            padding: 0.5rem;
            border-radius: 0.5rem;
            color: var(--scroll-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;

            & p {
              font-weight: 700;
            }
          }

          & div.selected:hover {
            border-color: var(--border-hover-color);
          }

          & div.dark {
            border-color: var(--input-color);
            color: var(--background);
          }

          & li.list-wrapper {
            & span.document-name {
              font-weight: 400;
            }

            & span.document-name.dark {
              color: var(--header-color);
            }

            & span.document-name.active {
              color: var(--icon-active-color);
            }
          }

          & li.active {
            background-color: var(--component-active);
          }

          & li.active.dark {
            background-color: var(--dark-main-col-5);
          }

          & li.list-wrapper:hover span.document-name {
            color: var(--scroll-color);
          }
        }

        & div.button-wrapper {
          display: flex;
          align-items: center;
          column-gap: 0.5rem;
        }
      }

      & div.summary-wrapper {
        max-width: 300px;
        width: 100%;
        background-color: #fff;
        padding: 1rem;
        border-radius: 0.5rem;

        & h1 {
          font-weight: bold;
          font-size: 1.2rem;
        }

        & div.selected-route-wrapper {
          margin-top: 1rem;

          & p {
            display: inline-block;
            padding-inline: 0.5rem;
            margin: 0.2rem;
            cursor: pointer;
            border-radius: 1rem;
            border: 1px solid lightgray;
          }
        }
      }
    }

    & div.select-route {
      padding: 2rem;
      border-radius: 1rem;
      max-width: 50%;
      width: 100%;
      background-color: white;
    }

    & div.select-route.dark {
      background-color: var(--dark-main-col-7);
    }
  }

  div.program-head {
    display: flex;
    align-items: center;
    column-gap: 1rem;
  }

  div.selected-wrapper {
    position: relative;
    margin-bottom: 1rem;
    width: 100%;

    & p.routes {
      padding: 0 0.5rem;
      transition: all ease-in-out 500ms;
      color: var(--input-color);
    }

    & p.routes.dark {
      color: var(--header-color);
    }

    & div.selected {
      transition: all ease-in-out 300ms;
      border: 1px solid var(--header-color);
      padding: 0.5rem;
      border-radius: 0.5rem;
      color: var(--scroll-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;

      & p {
        font-weight: 700;
      }
    }

    & div.selected:hover {
      border-color: var(--border-hover-color);
    }

    & div.dark {
      border-color: var(--input-color);
      color: var(--background);
    }

    & li.list-wrapper {
      & span.document-name {
        font-weight: 400;
      }

      & span.document-name.dark {
        color: var(--header-color);
      }

      & span.document-name.active {
        color: var(--icon-active-color);
      }
    }

    & li.active {
      background-color: var(--component-active);
    }

    & li.active.dark {
      background-color: var(--dark-main-col-5);
    }

    & li.list-wrapper:hover span.document-name {
      color: var(--scroll-color);
    }
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

  div.register-document-wrapper {
    padding: 2rem;
    height: 100%;

    & span {
      font-size: 1rem;
      font-weight: 700;
      color: var(--scroll-color);
      transition: all ease-in-out 300ms;
    }

    & span.dark {
      color: var(--icon-dark);
    }

    & form {
      display: flex;
      justify-content: center;
      column-gap: 10rem;
      height: 100%;

      & div.credential-wrapper {
        width: 100%;
        position: relative;

        & div.select-wrapper {
          column-gap: 1rem;
          align-items: start;
          display: flex;
        }

        & div.select-wrapper button {
          width: 15rem;
          height: 2.6rem;
        }

        & textarea {
          outline: none;
          transition: 300ms;
          background-color: transparent;
          border-radius: 0.5rem;
          padding: 0.5rem;
          width: 100%;
          height: 74%;
          min-width: 20%;
          min-height: 20%;
          border: 1px solid var(--header-color);
          color: var(--scroll-color);
        }

        & textarea.dark {
          border-color: var(--input-color);
          color: var(--background);
        }

        & textarea.dark::placeholder {
          color: var(--background);
        }

        & textarea:hover {
          border-color: var(--border-hover-color);
        }

        & textarea:focus {
          border-color: var(--border-active-color);
        }

        & div.code-wrapper {
          margin-top: 1rem;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: space-between;

          & div.code-placeholder {
            overflow: hidden;
            position: relative;
            border-radius: 1rem;
            transition: all ease-in-out 300ms;
            background-color: var(--main-col-1);
            width: 15rem;
            height: 15rem;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;

            & span.qr-label {
              transition: color ease-in-out 300ms;
              color: var(--background);
              margin: auto;
              font-weight: normal;
              font-size: 0.9rem;
            }

            & img.qrcode {
              border-radius: 0.5rem;
            }

            & div.code-overlap {
              position: absolute;
              transition: all ease-in-out 300ms;
              inset: 0;
              display: flex;
              justify-content: center;
              align-items: center;
              z-index: 2;

              & span.download-qr {
                color: var(--background);
              }
            }

            & div.code-overlap:hover {
              background-color: rgba(84, 84, 84, 0.9);
            }
          }

          & div.dark {
            background-color: var(--dark-main-col-2);
          }

          & div.code-placeholder:hover {
            background-color: var(--main-col-2);
            box-shadow: 1px 2px 3px var(--main-col-2);
          }

          & div.dark:hover {
            background-color: var(--navigation-hover-dark);
            box-shadow: none;
          }

          & div.code-placeholder:hover span.qr-label {
            color: var(--scroll-color);
          }

          & div.dark:hover span.qr-label {
            color: var(--background);
          }
        }

        & div.button-wrapper {
          display: flex;
          justify-content: flex-end;

          & div.button {
            display: flex;
            column-gap: 1rem;
            width: 22rem;
            margin-top: 1rem;
          }
        }
      }

      & div.code-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;

        & span {
          font-size: 1rem;
          font-weight: 700;
          color: var(--scroll-color);
          transition: all ease-in-out 300ms;
        }

        & span.dark {
          color: var(--icon-dark);
        }

        & div.code-placeholder {
          overflow: hidden;
          position: relative;
          border-radius: 1rem;
          transition: all ease-in-out 300ms;
          background-color: var(--main-col-1);
          width: 15rem;
          height: 15rem;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;

          & span.qr-label {
            transition: color ease-in-out 300ms;
            color: var(--background);
            margin: auto;
            font-weight: normal;
            font-size: 0.9rem;
          }

          & img.qrcode {
            border-radius: 0.5rem;
          }

          & div.code-overlap {
            position: absolute;
            transition: all ease-in-out 300ms;
            inset: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1;

            & span.download-qr {
              color: var(--background);
            }
          }

          & div.code-overlap:hover {
            background-color: rgba(84, 84, 84, 0.9);
          }
        }

        & div.dark {
          background-color: var(--dark-main-col-2);
        }

        & div.code-placeholder:hover {
          background-color: var(--main-col-2);
          box-shadow: 1px 2px 3px var(--main-col-2);
        }

        & div.dark:hover {
          background-color: var(--navigation-hover-dark);
          box-shadow: none;
        }

        & div.code-placeholder:hover span.qr-label {
          color: var(--scroll-color);
        }

        & div.dark:hover span.qr-label {
          color: var(--background);
        }
      }
    }
  }

  @media (max-width: 700px) {
    div.register-document-wrapper
      form.register-document-form
      div.credential-wrapper
      textarea {
      height: 30%;
    }

    div.register-document-wrapper
      form.register-document-form
      div.credential-wrapper
      div.code-wrapper
      div.code-placeholder {
      width: 100%;
    }
  }
</style>
