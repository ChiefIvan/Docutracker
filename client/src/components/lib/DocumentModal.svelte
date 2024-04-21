<script lang="ts">
  import {
    dark,
    documentDetails,
    detailsExpand,
    address,
    handleFetch,
    showMessage,
    filterName,
    location,
    userData,
    type RequestAPI,
    type ResponseData,
  } from "../../store";
  import { tooltip } from "../shared/Tooltip";
  import { fade } from "svelte/transition";

  import Button from "../shared/Button.svelte";
  import ArrowIcon from "../icons/ArrowIcon.svelte";
  import QrCode from "svelte-qrcode";

  export let authToken = "";
  export let route: string = "";

  let commentValue = "";
  let openComment = false;

  const approvalRequest: RequestAPI = {
    method: "POST",
    address: `${address}/document_approval`,
    credentials: {
      approval: "",
      unit: "",
      codeData: "",
      comment: "",
    },
  };

  const handleApproval = async (args: string) => {
    approvalRequest.credentials!.approval = args;
    approvalRequest.credentials!.unit = route;
    approvalRequest.credentials!.codeData = $documentDetails.documentD.codeData;
    approvalRequest.credentials!.comment = commentValue;

    const response: ResponseData = await handleFetch(
      approvalRequest,
      authToken
    );

    $showMessage = response;

    if (response.success) {
      $detailsExpand = false;

      setTimeout(() => {
        window.location.reload();
      }, 1000);
    }
  };

  const deleteRequest: RequestAPI = {
    method: "POST",
    address: `${address}/delete`,
    credentials: {
      codeData: "",
    },
  };

  const handleDelete = async () => {
    deleteRequest.credentials!.codeData = $documentDetails.documentD.codeData;

    try {
      await handleFetch(deleteRequest, authToken);
      setTimeout(() => {
        window.location.reload();
      }, 500);
    } catch (error) {
      console.error(error);
    }
  };

  $: lastRoute =
    $documentDetails.documentD.documentPath[
      $documentDetails.documentD.documentPath.length - 1
    ];

</script>

{#if openComment}
  <div class="comment-wrapper" transition:fade>
    <div
      class="back-wrapper"
      use:tooltip={{
        arrow: false,
        content: "Go Back",
        animation: "perspective-subtle",
        theme: "tooltip",
        offset: [-3, 20],
        placement: "left",
      }}
    >
      <ArrowIcon
        arrowState={true}
        dark={true}
        sizeMedium={true}
        on:click={() => (openComment = false)}
      ></ArrowIcon>
    </div>
    <form on:submit|preventDefault={() => handleApproval("disapproved")}>
      <textarea
        bind:value={commentValue}
        placeholder="Comment of Rejection (Mandatory)"
      ></textarea>
      <Button critical={true}>Reject</Button>
    </form>
  </div>
{/if}
<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
  transition:fade
  on:click={() => ($detailsExpand = false)}
  class="document-details-wrapper"
>
  <!-- <div
    class="back-wrapper"
    use:tooltip={{
      arrow: false,
      content: "Go Back",
      animation: "perspective-subtle",
      theme: "tooltip",
      offset: [-3, 20],
      placement: "left",
    }}
  >
    <ArrowIcon
      arrowState={true}
      dark={true}
      sizeMedium={true}
      on:click={() => ($detailsExpand = false)}
    ></ArrowIcon>
  </div> -->
  <div class="document-details">
    <div class="title-container">
      <h2 class="title">Document Details</h2>
      <!-- <span> Status: Pending to Forward </span> -->
    </div>
    {#if $documentDetails.userNameD && $documentDetails.emailD.length}
      <div class="content-wrapper">
        <div class="content">
          <p class:dark={$dark}>Author</p>
          <p class="value" class:dark={$dark}>{$documentDetails.userNameD}</p>
        </div>
        <div class="content">
          <p class:dark={$dark}>Email</p>
          <p class="value" class:dark={$dark}>{$documentDetails.emailD}</p>
        </div>
      </div>
    {/if}
    <div class="content-wrapper">
      {#if $documentDetails.documentD}
        <div class="content">
          <p>Document Name</p>
          <p class="value">{$documentDetails.documentD.documentName}</p>
        </div>
        <div class="content">
          <p>Document ID</p>
          <p class="value">{$documentDetails.documentD.codeData}</p>
        </div>
        <div class="content">
          <p>Submit Attemps</p>
          <p class="value">{$documentDetails.documentD.attemps}</p>
        </div>
        <div class="content">
          <p>Registered Date</p>
          <p class="value">{$documentDetails.documentD.pendingDate}</p>
        </div>
        {#if $documentDetails.documentD.documentPath && $documentDetails.documentD.documentPath.length}
          {#each $documentDetails.documentD.documentPath as path, i (i)}
            {#if (path.approved && path.confirmed) || path.finished}
              <div class="content">
                <p>
                  {i + 1} Route (Approved By)
                </p>
                <p class="value">{path.name}</p>
              </div>
            {/if}
            {#if !path.approved}
              <div class="content">
                <p>Rejected By</p>
                <p class="value">{path.name}</p>
              </div>
            {/if}
            {#if path.approved && !path.confirmed && path.finished && path.complete}
              <div class="content">
                <p>Completed By</p>
                <p class="value">{path.name}</p>
              </div>
            {/if}
          {/each}
        {/if}
      {/if}
    </div>
    <div class="des-code-wrapper">
      <div class="description-route-wrapper">
        <div class="description-wrapper">
          <p class="description">Route</p>
          <section>
            {#if $documentDetails.documentD.documentName === "Faculty Loading"}
              Program Head / Dean Office / Academic VP
            {:else if $documentDetails.documentD.documentName === "Requested Subject"}
              Program Head / Dean Office / Academic VP
            {:else if $documentDetails.documentD.documentName === "Application for Leave"}
              {#if $userData.previlage === "User"}
                {#if $userData.unit === "Program Head"}
                  Dean / HROS / VPAA
                {:else if $userData.unit === "Dean"}
                  HROS / VPAA
                {:else}
                  Program Head / HROS / VPAA
                {/if}
              {:else if $userData.previlage === "Secretary"}  
                {#if $userData.users && $userData.users.length}
                  {#each $userData.users as user, i (i)}
                    {#if $documentDetails.emailD === user.email}
                      {#if user.designation === "Program Head"}
                        Dean / HROS / VPAA
                      {:else if user.designation === "Dean"}
                        HROS / VPAA
                      {:else}
                        Program Head / HROS / VPAA
                      {/if}
                    {/if}
                  {/each}
                {/if}
              {/if}
            {:else}
              Program Head / Dean Office / Academic VP / OP
            {/if}
          </section>
        </div>
        <div class="description-wrapper">
          <p class="description">Description</p>
          <section>{$documentDetails.documentD.documentDescription}</section>
        </div>
        {#if $documentDetails.documentD.documentPath.length}
          {@const comment =
            $documentDetails.documentD.documentPath[
              $documentDetails.documentD.documentPath.length - 1
            ].comment}
          {#if comment}
            <div class="description-wrapper">
              <p class="description">Comment of Rejection</p>
              <section>{comment}</section>
            </div>
          {/if}
        {/if}
      </div>
      {#if $documentDetails.documentD.codeData}
        {@const value = $documentDetails.documentD.codeData}
        <div class="code-wrapper">
          <QrCode {value}></QrCode>
        </div>
      {/if}
    </div>
  </div>
  <div class="button-wrapper">
    {#if $userData.previlage !== "User"}
      {#if $documentDetails.documentD.documentPath.length}
        {#if lastRoute.approved && !lastRoute.confirmed && !lastRoute.finished}
          {#if $filterName == "Self"}
            {#if lastRoute.name === "Academic VP" || lastRoute.name === "Academic VP" || lastRoute.name === "VPAA" || lastRoute.name === "OP"}
              <Button hoverized={true} on:click={() => handleApproval("finish")}
                >Finish (Applicable for the last route)</Button
              >
            {:else}
              <Button
                hoverized={true}
                on:click={() => handleApproval("confirm")}>Confirm</Button
              >
            {/if}
          {/if}
        {:else if lastRoute.approved && lastRoute.finished && !lastRoute.complete}
          {#if $filterName === "Self"}
            <Button hoverized={true} on:click={() => handleApproval("complete")}
              >Complete</Button
            >
          {/if}
        {:else if lastRoute.confirmed && !lastRoute.finished && !lastRoute.complete}
          <Button
            hoverized={true}
            critical={true}
            on:click={() => (openComment = !openComment)}>Reject</Button
          >
          <Button hoverized={true} on:click={() => handleApproval("approved")}
            >Approved</Button
          >
        {/if}
      {:else if $userData.previlage === "Secretary"}
        <Button
          hoverized={true}
          critical={true}
          on:click={() => (openComment = !openComment)}>Reject</Button
        >
        <Button hoverized={true} on:click={() => handleApproval("approved")}
          >Approved</Button
        >
      {/if}
    {/if}
    {#if $userData.previlage === "User"}
      {#if lastRoute && !lastRoute.approved}
        <Button hoverized={true} on:click={() => handleApproval("resubmit")}
          >Re-Submit</Button
        >
      {/if}
    {/if}
    <!-- {#if $location === "/history"}
      <Button hoverized={true} critical={true} on:click={handleDelete}
        >Delete this Process</Button
      >
    {/if} -->
  </div>
</div>

<style>
  div.comment-wrapper {
    position: fixed;
    inset: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    row-gap: 0.5rem;
    z-index: 11;
    background-color: rgba(0, 0, 0, 0.7);

    & div.back-wrapper {
      max-width: 30rem;
      width: 100%;
    }

    & form {
      max-width: 30rem;
      width: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      row-gap: 0.5rem;

      & textarea {
        width: inherit;
        height: 10rem;
        margin-bottom: 0.5rem;
        outline: none;
        padding: 0.5rem;
        border: 1px solid var(--header-color);
        border-radius: 0.5rem;
      }
    }
  }

  div.document-details-wrapper {
    position: fixed;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.7);
    z-index: 5;
    display: flex;
    flex-direction: column;
    row-gap: 1rem;
    justify-content: center;
    align-items: center;

    & div.back-wrapper {
      width: 50rem;
    }

    & div.document-details {
      border-radius: 0.5rem;
      max-width: 50rem;
      width: 100%;
      padding: 1rem;
      background-color: var(--background);

      & div.title-container {
        padding: 0.3rem;
        border-bottom: 1px solid var(--header-color);

        & h2.title {
          font-size: 1.2rem;
          font-weight: bold;
          color: var(--main-col-3);
        }

        & span {
          color: var(--header-color);
        }
      }

      & div.content-wrapper {
        border-bottom: 1px solid var(--header-color);
        padding: 0.5rem 0.3rem;

        & div.content {
          display: flex;
          justify-content: space-between;

          & p {
            color: var(--scroll-color);
          }

          & p.value {
            color: var(--scroll-color);
            font-weight: bold;
          }

          & p.dark {
            color: var(--main-col-3);
          }
        }
      }

      & div.des-code-wrapper {
        display: flex;
        column-gap: 2rem;

        & div.description-route-wrapper {
          flex: 2;

          & div.description-wrapper {
            padding-top: 1rem;

            & p.description {
              font-size: 1.1rem;
              font-weight: bold;
              color: var(--main-col-3);
            }
          }
        }

        & div.code-wrapper {
          border-radius: 1rem;
          margin-top: 1rem;
          padding: 0.5rem;
          background-color: var(--main-col-1);
          display: flex;
          align-items: center;
        }

        & div.code-wrapper > * {
          border-radius: 0.5rem;
        }
      }
    }

    & div.button-wrapper {
      display: flex;
      justify-content: end;
      column-gap: 1rem;
      width: 50rem;
    }
  }
</style>
