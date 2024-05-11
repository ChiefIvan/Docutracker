<script lang="ts">
  import { dark, type Document } from "../../store";
  import { scale } from "svelte/transition";
  import { createEventDispatcher } from "svelte";

  import moment from "moment";
  import Button from "../shared/Button.svelte";
  import QrCode from "svelte-qrcode";
  import pdfMake from "pdfmake/build/pdfmake";
  import pdfFonts from "pdfmake/build/vfs_fonts";

  pdfMake.vfs = pdfFonts.pdfMake.vfs;

  export let theDocument: Document;

  const dispatch = createEventDispatcher();

  const handleClose = () => {
    dispatch("close");
  };

  let count = 0;
  let range: number[] = [];

  // let percentages = hours.map((value) => (value / maxV) * 100);

  while (24 > range.length) {
    range = [count, ...range];
    count++;
  }

  let timeData: {
    routeName: string;
    approvedDate: string;
    confirmedDate: string;
    durationInHours: number;
    hours: number;
    minutes: number;
    seconds: number;
  }[] = [];

  timeData = theDocument.documentPath
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

  const sampleGenerate = {
    content: [
      {
        text: `${theDocument.documentName}`,
        style: "header",
      },
      {
        layout: "lightHorizontalLines",
        margin: [0, 20, 0, 0],
        table: {
          widths: ["*", "*"],
          body: [
            [{ text: "Credentials", bold: true }, ""],
            ["Document Name", theDocument.documentName],
            ["Document ID", theDocument.codeData],
            ["Registered Date", theDocument.pendingDate],
            ["Submit Attemps", theDocument.attemps],
            ...theDocument.documentPath.map((path, i) => [
              `${i + 1} Route (Approved By)`,
              path.name,
            ]),
          ],
        },
      },
      {
        layout: "lightHorizontalLines",
        margin: [0, 20, 0, 0],
        table: {
          widths: ["*", "*"],
          body: [
            [{ text: "Time Taken", bold: true }, ""],
            ...theDocument.documentPath.map((path, i) => {
              const duration = moment.duration(moment(path.approvedDate, "ddd, DD MMM YYYY HH:mm:ss z").diff(moment(path.confirmedDate, "ddd, DD MMM YYYY HH:mm:ss z")))
              return [
                path.name,
                `${duration.hours()} hours, ${duration.minutes()} minutes, ${duration.seconds()} seconds`
              ];
            }),
          ],
        },
      },
      {
        layout: "noBorders",
        margin: [0, 30, 0, 0],
        table: {
          widths: ["*", "*"],
          body: [
            [{ text: "Document Description", bold: true }, ""],
            [
              theDocument.documentDescription,
              {
                qr: theDocument.codeData,
                background: "white",
                foreground: "#808080",
                fit: "200",
                margin: [80, -20, 0, 0],
              },
            ],
          ],
        },
      },
    ],
    styles: {
      header: {
        fontSize: 22,
        bold: true,
      },
    },
  };
</script>

<div class="wrapper" transition:scale>
  <div class="track-details-wrapper">
    <div class="tracking-details">
      <h1>Tracking Information</h1>
      <div class="track">
        {#each Array(theDocument.documentPath.length) as _, i (i)}
          {@const pathValue =
            theDocument.documentPath[theDocument.documentPath.length - 1 - i]}
          {#if pathValue.approved && pathValue.confirmed && pathValue.finished && pathValue.complete}
            <div class="info-wrapper">
              <div class="date-wrapper">
                <p class:dark={$dark}>{pathValue.completeDate}</p>
              </div>
              <div class="info">
                <h3 class:dark={$dark}>Status: Complete</h3>
                <span class:dark={$dark}
                  >This Document is waiting to be passed on to the next step in
                  the process and ready to be approve by the secretary of the
                  next route. Please proceed to that route as soon as possible.</span
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
                <h3 class:dark={$dark}>Status: Waiting for the recipient</h3>
                <span class:dark={$dark}
                  >Your document is finished and is waiting for you to claim
                  from {pathValue.name}. Please get your document immediately!</span
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
                  >This Document is waiting to be passed on to the next step in
                  the process and ready to be approve by the reciever of the
                  next route. Please proceed to that route as soon as possible.</span
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
                  >Lorem ipsum dolor, sit amet consectetur adipisicing elit.
                  Distinctio ut suscipit eaque temporibus iste error consequatur
                  necessitatibus dolor repellat odio.</span
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
                  has been approved, this signifies that the transaction is successful.</span
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
        {#if theDocument.pending}
          <div class="info-wrapper">
            <div class="date-wrapper">
              <p class:dark={$dark}>{document.pendingDate}</p>
            </div>
            <div class="info">
              <h3 class:dark={$dark}>
                Status: To be Forwarded
                <!-- {#if value.documentName === "Faculty Loading"}
                      Program Head
                    {/if} -->
              </h3>
              <span class:dark={$dark}
                >This Document is waiting to be passed on to the next step in
                the process and ready to be approve by the reciever of the first
                route. Please proceed to that route as soon as possible.</span
              >
            </div>
          </div>
        {/if}
      </div>
    </div>
    <div class="details-wrapper">
      <h1>Document Details</h1>

      <div class="details">
        <div class="detail">
          <p>Document Name:</p>
          <p>{theDocument.documentName}</p>
        </div>
        <div class="detail">
          <p>Document ID:</p>
          <p>{theDocument.codeData}</p>
        </div>
        <div class="detail">
          <p>Submit Attemps:</p>
          <p>{theDocument.attemps}</p>
        </div>
        <div class="detail">
          <p>Registered Data:</p>
          <p>{theDocument.pendingDate}</p>
        </div>
        {#each theDocument.documentPath as path, i (i)}
          <div class="detail">
            <p>
              {i + 1} Route (Approved By)
            </p>
            <p>{path.name}</p>
          </div>
        {/each}
      </div>
      <div class="des-qr-wrapper">
        <div class="des">
          <p>Document Description</p>
          <p>{theDocument.documentDescription}</p>
        </div>
        <div class="code-wrapper">
          <div class="code">
            <QrCode value={theDocument.codeData}></QrCode>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="details-s">
    <h1>Time Analysis</h1>
    <div class="wrappers">
      <div class="content-wrapper">
        <div class="lines-wrapper">
          {#each range as n}
            <div class="lines">{n}</div>
          {/each}
        </div>
        <div class="bar-wrapper">
          {#each timeData as value, index (index)}
            <div class="bars" style={`height: ${value.durationInHours}%;`}>
              <div class="bar-name">
                {value.routeName}
              </div>
            </div>
          {/each}
        </div>
      </div>
      <div class="summary-wrapper">
        <div>
          <h2>Route</h2>
          <ul class="time-wrapper">
            {#each timeData as value, index (index)}
              {#if value.hours && value.minutes}
                <li>
                  ✅ {value.routeName} took {value.hours} hours and {value.minutes}
                  minutes to confirm.
                </li>
              {:else if !value.hours && value.minutes && value.seconds}
                <li>
                  ✅ {value.routeName} took {value.minutes} minutes and {value.seconds}
                  seconds to confirm.
                </li>
              {:else if !value.hours && !value.minutes && value.seconds}
                <li>
                  ✅ {value.routeName} took {value.seconds} seconds to confirm.
                </li>
              {/if}
            {/each}
          </ul>
        </div>
        <div>
          <h2>Time</h2>
          <p>
            {#if theDocument && theDocument.documentPath && theDocument.documentPath.length}
              {@const firstRouteApprovedTime = moment(
                theDocument.documentPath[0].approvedDate,
                "ddd, DD MMM YYYY HH:mm:ss z"
              )}
              {@const lastRouteApprovedTime = moment(
                theDocument.documentPath[theDocument.documentPath.length - 1]
                  .completeDate,
                "ddd, DD MMM YYYY HH:mm:ss z"
              )}
              {@const totalTime = moment.duration(
                lastRouteApprovedTime.diff(firstRouteApprovedTime)
              )}
              {#if totalTime.hours() && totalTime.minutes()}
                Total transaction time: {totalTime.hours()} hours and
                {totalTime.minutes()} minutes
              {:else if !totalTime.hours() && totalTime.minutes() && totalTime.seconds()}
                Transaction time: {totalTime.minutes()} minutes and {totalTime.seconds()}
                seconds
              {:else if !totalTime.hours() && !totalTime.minutes() && totalTime.seconds()}
                Total transaction time: {totalTime.seconds()} seconds.
              {/if}
            {:else}
              This document hasn't been approved yet!
            {/if}
          </p>
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
  </div>
  <div class="btn-wrapper">
    <Button
      on:click={() => {
        pdfMake
          .createPdf(sampleGenerate)
          .download(`${theDocument.documentName}_${theDocument.codeData}`);
      }}>Save Data</Button
    >
    <Button on:click={handleClose}>Close</Button>
  </div>
</div>

<style>
  h1 {
    margin-bottom: 1rem;
    font-size: 1.5rem;
    font-weight: 900;
  }

  div.wrapper {
    position: fixed;
    inset: 0;
    z-index: 15;
    background-color: var(--background);
    padding: 1.5rem 16rem;
    overflow-y: auto;

    & div.btn-wrapper {
      margin-top: 5rem;
      width: 100%;
      display: flex;
      justify-content: flex-end;
      column-gap: 1rem;
    }

    & div.btn-wrapper > * {
      width: 15%;
      display: inline;
    }

    & div.track-details-wrapper {
      display: flex;
      column-gap: 5rem;

      & div.tracking-details {
        flex: 1;

        & div.track {
          height: 400px;
          overflow-y: auto;
          -webkit-mask: linear-gradient(white 20%, transparent);
          mask: linear-gradient(white 20%, transparent);
          padding: 2rem 2rem;
          padding-bottom: 10rem;

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
            }

            & div.info {
              position: relative;
              border-left: 1px solid var(--scroll-color);
              width: 20rem;
              padding: 0 2rem;

              & h3 {
                transition: all ease-in-out 300ms;
                font-size: 1.1rem;
                font-weight: bold;
                margin-bottom: 1rem;
              }

              & span {
                display: inline-block;
                padding-bottom: 3rem;
                color: var(--scroll-color);
                transition: all ease-in-out 300ms;
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
        }

        & div.track::-webkit-scrollbar {
          width: 0.5rem;
          height: 0.5rem;
        }

        & div.track::-webkit-scrollbar-track {
          background: var(--main-col-6);
        }

        & div.track::-webkit-scrollbar-thumb {
          background: var(--main-col-3);
        }

        & div.track::-webkit-scrollbar-thumb:hover {
          background: var(--scroll-color);
        }
      }

      & div.details-wrapper {
        flex: 1;

        & div.details {
          & div.detail {
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid var(--component-active);
            padding: 0.2rem 0;

            /* & p {
              font-size: 1.1rem;
            } */
          }

          & p:nth-child(1) {
            font-weight: 500;
          }
        }

        & div.des-qr-wrapper {
          display: flex;
          justify-content: space-between;
          margin-top: 2rem;

          & div.code {
            flex: 1;
            border-radius: 1rem;
            margin-top: 1rem;
            padding: 0.5rem;
            background-color: var(--main-col-1);
            display: flex;
            align-items: center;
          }

          & div.code > * {
            border-radius: 0.5rem;
          }

          & div.des {
            flex: 1;

            & p:nth-child(1) {
              font-size: 1.1rem;
              font-weight: 700;
            }
          }
        }
      }
    }

    & div.details-s {
      margin-top: 5rem;

      & div.wrappers {
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
              border-top: 1px solid rgba(0, 0, 0, 0.05);
              flex: 1;
              display: flex;
              align-items: center;
              color: var(--scroll-color);
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

              & div.bar-name {
                position: absolute;
                text-align: center;
                width: 100%;
                bottom: -2.5rem;
              }
            }
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
              color: var(--scroll-color);
            }

            & ul.time-wrapper {
              & li {
                display: inline-block;
              }
            }
          }
        }
      }
    }
  }
</style>
