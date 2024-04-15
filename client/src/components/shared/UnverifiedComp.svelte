<script>
  import { dark } from "../../store";

  import errorBanner from "./../../assets/pagenotfound_banner.png";
</script>

<div class="main">
  <div class="main-container">
    <img src={errorBanner} alt="page error banner" />
    <h1 class:dark={$dark}>Opps!</h1>
    <h3>Please wait for the admin to verify your account!</h3>
    <section class:dark={$dark}>
      <p>You need to be a fully registered user of Docutracker!</p>
      <p>To use its Features.</p>
    </section>
  </div>
</div>

<style>
  div.main {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;

    & div.main-container {
      text-align: center;
      min-width: 15rem;
      padding: 1rem;

      & img {
        width: -webkit-fill-available;
      }

      & h1 {
        transition: all ease-in-out 300ms;
        font-weight: bolder;
        font-size: 2.5rem;
        color: var(--main-col-3);
      }

      & h1.dark {
        color: var(--background);
      }

      & h3 {
        color: crimson;
        margin: 1rem;
        font-size: 1.5rem;
      }

      & section {
        transition: all ease-in-out 300ms;
        margin: 1.5rem 0;
        text-align: center;
        color: var(--main-col-3);
      }

      & section.dark {
        color: var(--main-col-7);
      }
    }
  }
</style>
