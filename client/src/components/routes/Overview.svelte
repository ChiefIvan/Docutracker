<script lang="ts">
  import { dark } from "../../store";
  import { navigate } from "svelte-routing";

  import Typewriter from "svelte-typewriter";
  import Footer from "../lib/Footer.svelte";
  import Button from "../shared/Button.svelte";

  const handleNavigate = (path: string) => {
    navigate(path);
  };
</script>

<svelte:head>
  <title>DOCUTRACKER | Overview</title>
</svelte:head>

<main>
  <div class="wrapper">
    <div class="typing">
      <Typewriter delay={1000}>Welcome to</Typewriter>
      <Typewriter
        mode={"scramble"}
        delay={2000}
        showCursorOnDelay={true}
        keepCursorOnFinish={true}>DOCUTRACKER</Typewriter
      >
    </div>
    <div class="button-wrapper" class:dark={$dark}>
      <span class:dark={$dark}>Get Started</span>
      <div class="buttons">
        <Button hoverized={true} on:click={() => handleNavigate("/auth/login")}
          >Login</Button
        >
        <Button hoverized={true} on:click={() => handleNavigate("/auth/signup")}
          >Signup</Button
        >
      </div>
    </div>
  </div>
  <Footer></Footer>
</main>

<style>
  main {
    position: fixed;
    inset: 0;
    display: flex;
    justify-content: space-evenly;
    flex-direction: column;

    & div.wrapper {
      width: 100%;
      text-align: center;

      & div.typing {
        height: 10rem;
        margin-bottom: 1rem;

        & div.typewriter-container > * {
          font-size: 2.3rem;
          font-weight: 900;
          color: var(--main-col-1);
        }
      }

      & div.button-wrapper {
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items: center;
        row-gap: 1rem;
        height: 20rem;
        background-color: var(--header-color);
        transition: all ease-in-out 500ms;

        & span {
          transition: all ease-in-out 300ms;
          font-size: 1.2rem;
          font-weight: 700;
        }

        & span.dark {
          color: var(--background);
        }

        & div.buttons {
          display: flex;
          justify-content: center;
          align-items: center;
          column-gap: 1rem;
        }

        & div.buttons > * {
          width: 15rem;
        }
      }

      & div.dark {
        background-color: var(--dark-main-col-1);
      }
    }
  }
</style>
