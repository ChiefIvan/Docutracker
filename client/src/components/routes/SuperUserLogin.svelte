<script lang="ts">
  import {
    dark,
    address,
    handleFetch,
    showMessage,
    type Credentials,
    type RequestAPI,
    type ResponseData,
  } from "../../store";
  import { navigate } from "svelte-routing";

  import Button from "../shared/Button.svelte";
  import Input from "../shared/Input.svelte";
  import greet from "./../../assets/greet.png";
  import BarLoader from "../shared/BarLoader.svelte";
  import Captcha from "../lib/Captcha.svelte";
  import CheckBox from "../shared/CheckBox.svelte";

  let inputKeyBind = false;
  let inputPasswordBind = false;
  let email = "";
  let key = "";
  let isRequest = false;
  let emailVerified = true;
  let keyVerified = true;
  let emailPattern = new RegExp(
    "^[a-zA-Z0-9._%+-]{5,}@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
  );

  $: email && email.length && !emailPattern.test(email)
    ? (emailVerified = false)
    : (emailVerified = true);

  $: (key && key !== key.toUpperCase()) || (key.length && key.length <= 10)
    ? (keyVerified = false)
    : (keyVerified = true);

  let credentials: Credentials = {
    email: "",
    key: "",
  };

  const sUserLoginRequest = {
    method: "POST",
    address: `${address}/admin_login`,
    credentials: credentials,
  };

  let formBind: HTMLFormElement;

  const handleSubmit = async () => {
    isRequest = true;

    sUserLoginRequest.credentials.email = email;
    sUserLoginRequest.credentials.key = key;

    console.log(sUserLoginRequest);

    try {
      const request: ResponseData = await handleFetch(sUserLoginRequest);
      if (request.error) {
        $showMessage = request;
        isRequest = false;
        return;
      }

      sessionStorage.setItem("remember", request.remembered!);
      window.location.href = "/admin";
      // checkValue = false;
      // allVerified = false;
      // inputKeyBind = false;
      // inputPasswordBind = false;
      // formBind.reset();
      // (document.activeElement as HTMLElement).blur();
    } catch (error) {
      isRequest = false;
      console.error(error);
    }

    isRequest = false;
  };

  const handleInput = (event: Event) => {
    let target = event.target as HTMLInputElement;
    let id = target.id;

    if (id === "Email") {
      email = target.value;
    }

    if (id === "Password") {
      key = target.value;
    }
  };

  let allVerified = false;
  let captchaImage = "";
  let checkValue = false;

  $: if (key && key.length && email && email.length) {
    allVerified = keyVerified && emailVerified;
  }

  let newSuperUser = {
    email: "",
    captVerification: false,
  };

  const captchaRequest: RequestAPI = {
    method: "GET",
    address: `${address}/captcha`,
  };

  const handleCaptcha = async () => {
    try {
      const response: ResponseData = await handleFetch(captchaRequest);

      if (!response.captchaGETValue) {
        return;
      }

      captchaImage = response.captchaGETValue[0];
      sessionStorage.setItem("captchaID", response.captchaGETValue[1]);
    } catch (error) {
      console.error(error);
    }
  };

  let attemps = 3;

  const handleDispatch = (event: { detail: boolean }) => {
    checkValue = event.detail;
    newSuperUser.captVerification = checkValue;

    if (!checkValue) {
      attemps--;

      if (attemps <= 0) {
        attemps = 3;
        $showMessage = {
          error: "Captcha Verification failed!, please try again.",
        };
        captchaImage = "";

        return;
      }

      handleCaptcha();

      return;
    }

    attemps = 3;
    captchaImage = "";
  };
</script>

<svelte:head>
  <title>DOCUTRACKER | Admin Login</title>
</svelte:head>

{#if isRequest}
  <BarLoader></BarLoader>
{/if}

<main>
  {#if captchaImage.length !== 0}
    <Captcha {captchaImage} on:dispatch={handleDispatch} />
  {/if}
  <img src={greet} alt="Greetings to the Admin" />
  <form bind:this={formBind} on:submit|preventDefault={handleSubmit}>
    <h1 class:dark={$dark}>Hello Admin</h1>
    <Input
      inputType="email"
      inputName="Email"
      verifiedEntry={emailVerified}
      tooltipContent="Your Email must have more than 4 characters before the '@', and both '@' symbol and a top-level domain are mandatory!"
      on:input={handleInput}
      bind:focusedInput={inputKeyBind}
      dark={$dark}
    />
    <Input
      inputType="password"
      inputName="Password"
      verifiedEntry={keyVerified}
      tooltipContent="The password should be all capital letters and must be exact 11 characters!"
      on:input={handleInput}
      bind:focusedInput={inputPasswordBind}
      dark={$dark}
    />
    <div class="captcha-wrapper">
      <CheckBox
        disabled={checkValue ? true : !allVerified}
        checked={checkValue}
        checkboxName="I am not a robot"
        on:change={handleCaptcha}
      />
    </div>
    <!-- <Captcha></Captcha> -->
    <Button disabled={!checkValue}>Login</Button>
  </form>
</main>

<style>
  main {
    height: 90vh;
    display: flex;
    align-items: center;
    justify-content: center;

    & img {
      max-width: 30rem;
    }

    & form {
      max-width: 25rem;
      width: 100%;

      & h1 {
        color: var(--scroll-color);
        font-size: 2.5rem;
        font-weight: bold;
      }

      & h1.dark {
        color: var(--background);
      }

      & p {
        color: var(--scroll-color);
        margin-bottom: 2rem;
      }

      & p.dark {
        color: var(--main-col-1);
      }

      & div.captcha-wrapper {
        margin: 1.7rem 0;
      }
    }
  }
</style>
