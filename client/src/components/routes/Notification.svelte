<script lang="ts">
  import { notifications, dark } from "../../store";

  import moment from "moment";
  let now = moment(moment().format("ddd, DD MMM YYYY HH:mm:ss z"));

  // const data = [
  //   {
  //     title: "Approved",
  //     body: "Your Endorsement Form has been approved",
  //     time: "34",
  //   },
  //   {
  //     title: "Approved",
  //     body: "Your Endorsement Form has been approved",
  //     time: "34",
  //   },
  //   {
  //     title: "Approved",
  //     body: "Your Endorsement Form has been approved",
  //     time: "34",
  //   },
  //   {
  //     title: "Approved",
  //     body: "Your Endorsement Form has been approved",
  //     time: "34",
  //   },
  //   {
  //     title: "Approved",
  //     body: "Your Endorsement Form has been approved",
  //     time: "34",
  //   },
  //   {
  //     title: "Approved",
  //     body: "Your Endorsement Form has been approved",
  //     time: "34",
  //   },
  //   {
  //     title: "Approved",
  //     body: "Your Endorsement Form has been approved",
  //     time: "34",
  //   },
  //   {
  //     title: "Approved",
  //     body: "Your Endorsement Form has been approved",
  //     time: "34",
  //   },
  //   {
  //     title: "Approved",
  //     body: "Your Endorsement Form has been approved",
  //     time: "34",
  //   },
  //   {
  //     title: "Approved",
  //     body: "Your Endorsement Form has been approved",
  //     time: "34",
  //   },
  // ];
</script>

<div class="notifications">
  <h1 class:dark={$dark}>Notifications</h1>
  <ul class="notification-render">
    {#if $notifications.length}
      {#each $notifications.reverse() as notification, i (i)}
        {@const date = moment(notification.date, "ddd, DD MMM YYYY HH:mm:ss z")}
        {@const gapTime = moment.duration(now.diff(date))}
        <li class:dark={$dark}>
          <h2 class:dark={$dark}> 
            {notification.title}
          </h2>
          <p class:dark={$dark}>{notification.body}</p>
          <div class="date-wrapper">
            <span class:dark={$dark}>{date.format("MMMM Do YYYY")}</span>
            <span class:dark={$dark}>
              {#if gapTime.days()}
                {gapTime.days()}
                {#if gapTime.days() > 1}
                  days
                {:else}
                  day
                {/if}
              {/if}
              {#if gapTime.hours() && !gapTime.days()}
                {gapTime.hours()}
                {#if gapTime.hours() > 1}
                  hours
                {:else}
                  hour
                {/if}
              {/if}
              {#if gapTime.minutes() && !gapTime.hours() && !gapTime.days()}
                {gapTime.minutes()}
                {#if gapTime.minutes() > 1}
                  minutes
                {:else}
                  minute
                {/if}
              {/if}
              {#if gapTime.seconds() && !gapTime.minutes() && !gapTime.hours() && !gapTime.days()}
                {gapTime.seconds()}
                {#if gapTime.seconds() > 1}
                  seconds
                {:else}
                  second
                {/if}
              {/if}
              ago
            </span>
          </div>
        </li>
      {/each}
    {:else}
      <li>
        <p class="no-noti" class:dark={$dark}>
          You don't have any notifications yet!
        </p>
      </li>
    {/if}
  </ul>
</div>

<style>
  div.notifications {
    padding: 0.5rem;

    & h1 {
      font-size: 1rem;
      font-weight: bold;
      color: var(--scroll-color);
      border-bottom: 1px solid var(--header-color);
      padding-bottom: 0.2rem;
      transition: color ease-in-out 300ms;
    }

    & h1.dark {
      color: var(--background);
      border-bottom-color: var(--main-col-1);
    }

    & ul {
      overflow-y: auto;
      height: 87vh;
      overflow-x: hidden;
      padding: 0.5rem;

      & li {
        & h2 {
          font-weight: bold;
          color: var(--scroll-color);
        }

        & h2.dark {
          color: var(--background);
        }

        & p {
          color: var(--main-col-1);
        }

        & p.dark {
          color: var(--header-color);
        }

        & div.date-wrapper {
          display: flex;
          justify-content: space-between;
          margin-bottom: 0.5rem;

          & span {
            display: block;
            text-align: end;
            font-size: 0.6rem;
            color: var(--main-col-7);
          }

          & span.dark {
            color: var(--main-col-1);
          }
        }

        & p.no-noti {
          text-align: center;
        }

        & p.dark {
          color: var(--header-color);
        }
      }
    }

    & ul::-webkit-scrollbar {
      width: 0.5rem;
      height: 0.5rem;
    }

    & ul::-webkit-scrollbar-track {
      background: var(--main-col-6);
    }
    & ul::-webkit-scrollbar-thumb {
      background: var(--main-col-3);
    }
    & ul::-webkit-scrollbar-thumb:hover {
      background: var(--scroll-color);
    }
  }
</style>
