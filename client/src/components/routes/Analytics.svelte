<script lang="ts">
  import { documents, dark, type Document } from "../../store";
  import { onMount } from "svelte";

  import moment from "moment";
  import CheckAuthenticity from "../shared/CheckAuthenticity.svelte";

  export let authToken = "";

  let count = 0;
  let range: number[] = [];

  // let hours = [4, 2, 7, 6, 10, 20];
  // let maxV = Math.max(...hours);
  // let percentages = hours.map((value) => (value / maxV) * 100);

  while (24 > range.length) {
    range = [count, ...range];
    count++;
  }

  let docN = "";
  let docid = "";

  onMount(() => {
    docid = localStorage.getItem("docid") || "";

    let documentExistance = $documents.filter(
      (document) => document.documentName === localStorage.getItem("docN")
    );

    if (documentExistance.length) {
      docN = localStorage.getItem("docN") || "";
      docid = localStorage.getItem("docid") || "";
    }
  });

  $: selectedDocument = $documents.find((document: Document): Document => {
    return document.codeData === docid;
  });

  $: console.log(selectedDocument);

  // let timeData = [
  //   {
  //     routeName: "Program Head",
  //     durationInHours: 34,
  //     hours: 2,
  //     minutes: 34,
  //     seconds: 25,
  //   },
  //   {
  //     routeName: "Dean Office",
  //     durationInHours: 78,
  //     hours: 7,
  //     minutes: 12,
  //     seconds: 45,
  //   },
  //   {
  //     routeName: "OP",
  //     durationInHours: 23,
  //     hours: 3,
  //     minutes: 56,
  //     seconds: 23,
  //   },
  //   {
  //     routeName: "VP",
  //     durationInHours: 38,
  //     hours: 1,
  //     minutes: 36,
  //     seconds: 21,
  //   },
  // ];

  let timeData: {
    routeName: string;
    approvedDate: string;
    confirmedDate: string;
    durationInHours: number;
    hours: number;
    minutes: number;
    seconds: number;
  }[] = [];
  $: console.log(timeData);

  $: if (
    selectedDocument &&
    selectedDocument.documentPath &&
    selectedDocument.documentPath.length
  ) {
    timeData = selectedDocument.documentPath
      .filter((route) => route.approvedDate && route.confirmedDate)
      .map((route) => {
        let approvedDate = moment(
          route.approvedDate,
          "ddd, DD MMM YYYY HH:mm:ss z"
        );
        let confirmedDate = moment(
          route.confirmedDate,
          "ddd, DD MMM YYYY HH:mm:ss z"
        );
        let duration = moment.duration(confirmedDate.diff(approvedDate));
        let hours = parseFloat(duration.asHours().toFixed(2));

        return {
          routeName: route.name,
          approvedDate: route.approvedDate,
          confirmedDate: route.confirmedDate,
          durationInHours: hours,
          hours: duration.hours(),
          minutes: duration.minutes(),
          seconds: duration.seconds(),
        };
      });

    console.log(timeData);
  }
</script>

<svelte:head>
  <title>DOCUTRACKER | Time Analysis</title>
</svelte:head>

<CheckAuthenticity {authToken} on:user></CheckAuthenticity>

<main>
  {#if timeData.length}
    <h1 class:dark={$dark}>
      {docN}
    </h1>
    <div class="wrapper">
      <div class="content-wrapper">
        <div class="lines-wrapper">
          {#each range as n}
            <div class="lines" class:dark={$dark}>{n}</div>
          {/each}
        </div>
        <div class="bar-wrapper" class:dark={$dark}>
          {#each timeData as value, index (index)}
            <div
              class="bars"
              class:dark={$dark}
              style={`height: ${value.durationInHours}%;`}
            >
              <div class="bar-name" class:dark={$dark}>
                {value.routeName}
              </div>
            </div>
          {/each}
        </div>
      </div>
      <div class="summary-wrapper">
        <div>
          <h2 class:dark={$dark}>Route</h2>
          <ul class="time-wrapper">
            {#each timeData as value, index (index)}
              {#if value.hours && value.minutes}
                <li class:dark={$dark}>
                  ✅ {value.routeName} took {value.hours} hours and {value.minutes}
                  minutes to confirm.
                </li>
              {:else if !value.hours && value.minutes && value.seconds}
                <li class:dark={$dark}>
                  ✅ {value.routeName} took {value.minutes} minutes and {value.seconds}
                  seconds to confirm.
                </li>
              {:else if !value.hours && !value.minutes && value.seconds}
                <li class:dark={$dark}>
                  ✅ {value.routeName} took {value.seconds} seconds to confirm.
                </li>
              {/if}
            {/each}
          </ul>
        </div>
        <div>
          {#if selectedDocument && selectedDocument.documentPath && selectedDocument.documentPath.length}
            {@const firstRouteApprovedTime = moment(
              selectedDocument.documentPath[0].approvedDate,
              "ddd, DD MMM YYYY HH:mm:ss z"
            )}
            {@const lastRouteApprovedTime = moment(
              selectedDocument.documentPath[
                selectedDocument.documentPath.length - 1
              ].completeDate,
              "ddd, DD MMM YYYY HH:mm:ss z"
            )}
            {@const totalTime = moment.duration(
              lastRouteApprovedTime.diff(firstRouteApprovedTime)
            )}
            {#if totalTime.hours() && totalTime.minutes()}
              <h2 class:dark={$dark}>Time</h2>
              <p class:dark={$dark}>
                {docN} got a total transaction time of {totalTime.hours()} hours
                and
                {totalTime.minutes()} minutes
              </p>
            {:else if !totalTime.hours() && totalTime.minutes() && totalTime.seconds()}
              <h2 class:dark={$dark}>Time</h2>
              <p class:dark={$dark}>
                {docN} got a total transaction time of {totalTime.minutes()} minutes
                and {totalTime.seconds()} seconds
              </p>
            {:else if !totalTime.hours() && !totalTime.minutes() && totalTime.seconds()}
              <h2 class:dark={$dark}>Time</h2>
              <p class:dark={$dark}>
                {docN} got a total transaction time of {totalTime.seconds()} seconds.
              </p>
            {/if}
          {:else}
            This document hasn't been approved yet!
          {/if}
        </div>
        <!-- <div>
          <h2>Summary</h2>
          <p> -->
        <!-- This section keeps track of the time taken by each route for the
          specific document you’ve chosen. -->
        <!-- Lorem ipsum dolor sit, amet consectetur adipisicing elit. Dolor officiis
            quisquam omnis? Assumenda ab reprehenderit labore distinctio similique
            modi odit numquam laborum nobis velit doloribus voluptatum dolores, mollitia,
            rerum voluptate at suscipit quaerat nostrum. Minima!
          </p>
        </div> -->
      </div>
    </div>
  {:else}
    <h1 class:dark={$dark} class:not={!docN && !docN.length}>
      {docN && docN.length
        ? `${docN} hasn't been confirmed yet!`
        : "Please select a document first"}
    </h1>
  {/if}
</main>

<style>
  main {
    margin: auto;
    max-width: 1000px;

    & h1 {
      font-size: 3rem;
      font-weight: bold;
      margin: 2rem 0;
      color: var(--scroll-color);
      transition: all ease-in-out 300ms;
    }

    & h1.not {
      text-align: center;
      line-height: 75vh;
    }

    & h1.dark {
      color: var(--background);
    }

    & div.wrapper {
      display: flex;
      /* align-items: center; */
      justify-content: center;
      column-gap: 2rem;

      & div.content-wrapper {
        position: relative;

        & div.lines-wrapper {
          display: flex;
          flex-direction: column;
          width: 42rem;
          height: 34.4rem;
          position: absolute;
          left: -2rem;
          padding: 0.5rem;
          z-index: -1;
          bottom: 0;

          & div.lines {
            border-bottom: 1px solid rgba(0, 0, 0, 0.05);
            flex: 1;
            display: flex;
            align-items: center;
            color: var(--scroll-color);
            transition: all ease-in-out 300ms;
          }

          & div.lines.dark {
            border-color: var(--dark-main-col-6);
            color: var(--main-col-2);
          }
        }

        & div.bar-wrapper {
          height: 35rem;
          width: 40rem;
          display: flex;
          column-gap: 0.5rem;
          align-items: flex-end;
          border-left: 1px solid var(--header-color);
          border-bottom: 1px solid var(--header-color);
          padding: 0.5rem;

          & div.bars {
            flex: 1;
            background-color: var(--header-color);
            position: relative;
            transition: all ease-in-out 300ms;

            & div.bar-name {
              transition: all ease-in-out 300ms;
              position: absolute;
              text-align: center;
              width: 100%;
              bottom: -2.5rem;
            }

            & div.bar-name.dark {
              color: var(--main-col-2);
            }
          }

          & div.bars.dark {
            background-color: var(--background);
          }
        }

        & div.bar-wrapper.dark {
          border-color: var(--input-color);
        }
      }

      & div.summary-wrapper {
        max-width: 25rem;
        width: 100%;
        display: flex;
        flex-direction: column;
        row-gap: 1.5rem;

        & div {
          & h2 {
            font-size: 1rem;
            font-weight: bold;
            transition: all ease-in-out 300ms;
            color: var(--scroll-color);
          }

          & h2.dark {
            color: var(--background);
          }

          & p {
            transition: all ease-in-out 300ms;
          }

          & p.dark {
            color: var(--main-col-2);
          }

          & ul.time-wrapper {
            & li {
              display: inline-block;
              transition: all ease-in-out 300ms;
            }

            & li.dark {
              color: var(--main-col-2);
            }
          }
        }
      }
    }
  }
</style>
