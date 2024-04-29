<script lang="ts">
  import { Link, navigate } from "svelte-routing";
  import { fly, fade } from "svelte/transition";
  // import { quintInOut } from "svelte/easing";

  // import { blobToBase64 } from "../shared/ImageConverter";
  import {
    type RequestAPI,
    type ResponseData,
    type SignUpBind,
    type Credentials,
    handleFetch,
    address,
    showMessage,
    dark,
  } from "../../store";

  import Input from "../shared/Input.svelte";
  import Button from "../shared/Button.svelte";
  import CheckBox from "../shared/CheckBox.svelte";
  import Captcha from "../lib/Captcha.svelte";
  import BarLoader from "../shared/BarLoader.svelte";
  import Cropper from "svelte-easy-crop";
  import EditIcon from "../icons/EditIcon.svelte";
  import CheckIcon from "../icons/CheckIcon.svelte";
  import UserIcon from "../../assets/user-icon.png";

  let fileData: FileList;
  let base64String: string | null;
  let pixelCrop: { width: number; height: number; x: number; y: number };
  let fileName = "Upload Your Profile";
  let croppedImage: string | null;
  let crop: { x: number; y: number };
  let zoom = 1;

  function handleImage() {
    croppedImage = null;
    zoom = 1;
    crop = { x: 0, y: 0 };

    let files = fileData[0];
    fileName = files.name;
    const reader = new FileReader();

    reader.onload = function (e) {
      if (typeof e.target!.result === "string") {
        base64String = e.target!.result;
      } else {
        console.warn("Event target is an Array Buffer at line 33");
      }
    };

    reader.readAsDataURL(files);
  }

  const createImage = (url: string) =>
    new Promise((resolve, reject) => {
      const image = new Image();
      image.addEventListener("load", () => resolve(image));
      image.addEventListener("error", (error) => reject(error));
      image.setAttribute("crossOrigin", "anonymous");
      image.src = url;
    });

  function getRadianAngle(degreeValue: number) {
    return (degreeValue * Math.PI) / 180;
  }

  export async function getCroppedImg(
    imageSrc: string | null,
    pixelCrop: { width: any; height: any; x: any; y: any },
    rotation = 0
  ): Promise<string> {
    const image = (await createImage(imageSrc!)) as HTMLImageElement;
    const canvas: HTMLCanvasElement = document.createElement("canvas");
    const ctx: CanvasRenderingContext2D = canvas.getContext("2d")!;

    const maxSize = Math.max(image.width, image.height);
    const safeArea = 2 * ((maxSize / 2) * Math.sqrt(2));

    canvas.width = safeArea;
    canvas.height = safeArea;

    ctx.translate(safeArea / 2, safeArea / 2);
    ctx.rotate(getRadianAngle(rotation));
    ctx.translate(-safeArea / 2, -safeArea / 2);

    ctx.drawImage(
      image,
      safeArea / 2 - image.width * 0.5,
      safeArea / 2 - image.height * 0.5
    );
    const data = ctx.getImageData(0, 0, safeArea, safeArea);

    canvas.width = pixelCrop.width;
    canvas.height = pixelCrop.height;

    ctx.putImageData(
      data,
      Math.round(0 - safeArea / 2 + image.width * 0.5 - pixelCrop.x),
      Math.round(0 - safeArea / 2 + image.height * 0.5 - pixelCrop.y)
    );

    return new Promise((resolve) => {
      canvas.toBlob((file) => {
        resolve(URL.createObjectURL(file!));
      }, "image/png");
    });
  }

  export async function getRotatedImage(imageSrc: string, rotation = 0) {
    const image = (await createImage(imageSrc)) as HTMLImageElement;
    const canvas: HTMLCanvasElement = document.createElement("canvas");
    const ctx: CanvasRenderingContext2D = canvas.getContext("2d")!;

    const orientationChanged =
      rotation === 90 ||
      rotation === -90 ||
      rotation === 270 ||
      rotation === -270;
    if (orientationChanged) {
      canvas.width = image.height;
      canvas.height = image.width;
    } else {
      canvas.width = image.width;
      canvas.height = image.height;
    }

    ctx.translate(canvas.width / 2, canvas.height / 2);
    ctx.rotate((rotation * Math.PI) / 180);
    ctx.drawImage(image, -image.width / 2, -image.height / 2);

    return new Promise((resolve) => {
      canvas.toBlob((file) => {
        resolve(URL.createObjectURL(file!));
      }, "image/webp");
    });
  }

  let bindForm: HTMLFormElement;
  let checkValue = false;
  let isRequest = false;

  let allVerified = false;
  let fullNameVerified = false;
  let instituteVerified = true;
  let emailVerified = true;
  let employeeIDVerified = true;
  let unitVerified = true;
  let passwordVerified = true;
  let cnfrmPasswordVerified = true;
  let othersRev = false;

  let emailPattern = new RegExp(
    "^[a-zA-Z0-9._%+-]{5,}@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
  );
  let passwordPattern = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).*$");
  let employeeIDPattern = new RegExp("^[0-9]{6}-[0-9]{3}$");

  let newUser: Credentials = {
    userImg: "",
    fullName: "",
    email: "",
    institute: "",
    employeeID: "",
    unit: "",
    password: "",
    cnfrmPassword: "",
    captVerification: false,
  };

  $: newUser.fullName && newUser.fullName.length && newUser.fullName.length < 8
    ? (fullNameVerified = false)
    : (fullNameVerified = true);

  $: newUser.email && newUser.email.length && !emailPattern.test(newUser.email)
    ? (emailVerified = false)
    : (emailVerified = true);

  $: newUser.employeeID &&
  newUser.employeeID.length &&
  !employeeIDPattern.test(newUser.employeeID)
    ? (employeeIDVerified = false)
    : (employeeIDVerified = true);

  $: newUser.unit && newUser.unit.length && newUser.unit.length < 4
    ? (unitVerified = false)
    : (unitVerified = true);

  $: (newUser.password &&
    newUser.password.length &&
    newUser.password.length < 8) ||
  (newUser.password &&
    newUser.password.length &&
    !passwordPattern.test(newUser.password))
    ? (passwordVerified = false)
    : (passwordVerified = true);

  $: newUser.cnfrmPassword &&
  newUser.cnfrmPassword.length &&
  newUser.password !== newUser.cnfrmPassword
    ? (cnfrmPasswordVerified = false)
    : (cnfrmPasswordVerified = true);

  $: if (
    newUser.fullName &&
    newUser.fullName.length &&
    newUser.email &&
    newUser.email.length &&
    newUser.employeeID &&
    newUser.employeeID.length &&
    newUser.unit &&
    newUser.unit.length &&
    newUser.institute &&
    newUser.institute.length &&
    newUser.password &&
    newUser.password.length &&
    newUser.cnfrmPassword &&
    newUser.cnfrmPassword.length
  ) {
    allVerified =
      fullNameVerified &&
      instituteVerified &&
      emailVerified &&
      employeeIDVerified &&
      unitVerified &&
      passwordVerified &&
      cnfrmPasswordVerified;
  }

  let inputBinds: SignUpBind = {
    fullNameInput: false,
    emailInput: false,
    employeeIDInput: false,
    unitInput: false,
    passwordInput: false,
    cnfrmPasswordInput: false,
    otherInput: false,
  };

  const handleInput = (event: Event) => {
    const target = event.target as HTMLInputElement;
    const id = target.id;

    if (id === "Fullname") {
      newUser.fullName = target.value;
    }

    if (id === "Email") {
      newUser.email = target.value;
    }

    if (id === "Employee ID") {
      newUser.employeeID = target.value;
    }

    if (id === "Password") {
      newUser.password = target.value;
    }

    if (id === "Confirm Password") {
      newUser.cnfrmPassword = target.value;
    }

    if (id === "N/A if None") {
      newUser.institute = target.value;
    }
  };

  const signUpAddress = `${address}/signup`;
  const signUpMethod = "POST";
  let timeOutID: number | undefined;

  let signUpRequest = {
    method: signUpMethod,
    address: signUpAddress,
    credentials: newUser,
  };

  const handleSubmit = async () => {
    if (!croppedImage || (croppedImage && !croppedImage.length)) {
      $showMessage = { error: "Please Select an Image for your Profile!" };
      return;
    }

    newUser.captVerification = checkValue;
    newUser.userImg = base64String;
    signUpRequest.credentials = newUser;

    isRequest = true;
    clearTimeout(timeOutID);

    try {
      localStorage.setItem("email", newUser.email!);
      const response: ResponseData = await handleFetch(signUpRequest);
      $showMessage = response;

      if (response.success) {
        bindForm.reset();

        checkValue = false;
        allVerified = false;

        newUser = {
          userImg: "",
          fullName: "",
          email: "",
          institute: "",
          employeeID: "",
          unit: "",
          password: "",
          cnfrmPassword: "",
          captVerification: false,
        };

        inputBinds = {
          fullNameInput: false,
          emailInput: false,
          employeeIDInput: false,
          unitInput: false,
          passwordInput: false,
          cnfrmPasswordInput: false,
          otherInput: false,
        };

        othersRev = false;

        navigate("/auth/login");
        timeOutID = setTimeout(() => {
          alert("If you can't see your Email, try checking out Spam Messages!");
        }, 1000);
      }
    } catch (error) {
      console.error(error);
      isRequest = false;
    }

    isRequest = false;
  };

  const captchaAddress = `${address}/captcha`;
  const captchaMethod = "GET";

  const captchaRequest: RequestAPI = {
    method: captchaMethod,
    address: captchaAddress,
  };

  let captchaImage = "";

  const handleCaptcha = async () => {
    try {
      const response: ResponseData = await handleFetch(captchaRequest);

      if (!response.captchaGETValue) {
        console.error("Captcha GET Values are undefined");
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
    newUser.captVerification = checkValue;

    if (!checkValue) {
      attemps--;

      if (attemps <= 0) {
        attemps = 3;
        console.warn("Captcha Verification failed!, please try again.");
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

  const handleRadio = (event: Event) => {
    const target = event.target as HTMLInputElement;
    newUser.institute = target.value;
  };

  $: console.log(newUser.institute);
</script>

<svelte:head>
  <title>DOCUTRACKER | Signup</title>
</svelte:head>

{#if isRequest}
  <BarLoader />
{/if}

{#if captchaImage.length !== 0}
  <Captcha {captchaImage} on:dispatch={handleDispatch} />
{/if}

<main>
  <!-- <h1 class:dark={$dark}>Sign up</h1> -->
  <div class="profile-image-wrapper">
    <div class="cropper-wrapper">
      {#if base64String}
        <!-- svelte-ignore a11y-img-redundant-alt -->
        {#if croppedImage}
          <img
            class="final-user-picture"
            transition:fade={{ duration: 300, delay: 0 }}
            src={croppedImage}
            alt="User Image"
          />
        {:else}
          <Cropper
            image={base64String}
            bind:crop
            bind:zoom
            cropShape="round"
            aspect={1}
            on:cropcomplete={(e) => (pixelCrop = e.detail.pixels)}
          />
        {/if}
      {:else}
        <img
          class="user-icon-wrapper"
          src={UserIcon}
          alt="User Anonymous Icon"
        />
      {/if}
    </div>
    <h3 class:dark={$dark} transition:fade={{ duration: 300, delay: 200 }}>
      {fileName}
    </h3>
    <div class="image-wrapper">
      <label for="image_upload">
        <EditIcon />
      </label>
      <CheckIcon
        on:click={async () => {
          croppedImage = await getCroppedImg(base64String, pixelCrop);
        }}
      />
    </div>
  </div>
  <form
    bind:this={bindForm}
    on:submit|preventDefault={handleSubmit}
    autocomplete="off"
  >
    <h1 class:dark={$dark}>Sign Up</h1>
    <input
      id="image_upload"
      name="User Image"
      bind:files={fileData}
      on:change={handleImage}
      type="file"
      accept=".jpg, .jpeg, .png"
    />
    <Input
      inputType="email"
      inputName="Email"
      verifiedEntry={emailVerified}
      tooltipContent="Your Email must have more than 4 characters before the '@', and both '@' symbol and a top-level domain are mandatory!"
      on:input={handleInput}
      bind:focusedInput={inputBinds.emailInput}
      dark={$dark}
      overlap={true}
    />

    <div class="input-center-wrapper">
      <Input
        inputType="text"
        inputName="Fullname"
        verifiedEntry={fullNameVerified}
        tooltipContent="Your Fullname must be greater than 8 characters!"
        on:input={handleInput}
        bind:focusedInput={inputBinds.fullNameInput}
        dark={$dark}
        overlap={true}
      />
      <Input
        inputType="text"
        inputName="Employee ID"
        verifiedEntry={employeeIDVerified}
        tooltipContent="Your employee ID must follow this pattern: '123456-789' six digits on the left side and 3 digits on right side separated by '-' symbol!"
        on:input={handleInput}
        bind:focusedInput={inputBinds.employeeIDInput}
        dark={$dark}
        overlap={true}
      />
    </div>
    <div class="input-center-wrapper">
      <Input
        inputType="password"
        inputName="Password"
        verifiedEntry={passwordVerified}
        tooltipContent="Your Password must be greater than 7 characters and have atleat 1 uppercase, 1 lowercase and a number!"
        on:input={handleInput}
        bind:focusedInput={inputBinds.passwordInput}
        dark={$dark}
        overlap={true}
      />
      <Input
        inputType="password"
        inputName="Confirm Password"
        verifiedEntry={cnfrmPasswordVerified}
        tooltipContent="Your Password and Password Confirmation must be the same!"
        on:input={handleInput}
        bind:focusedInput={inputBinds.cnfrmPasswordInput}
        dark={$dark}
        overlap={true}
      />
    </div>

    <!-- <Input
        inputType="text"
        inputName="Designation"
        verifiedEntry={unitVerified}
        tooltipContent="Office/Designation must be greater than 4 characters!"
        on:input={handleInput}
        bind:focusedInput={inputBinds.unitInput}
        dark={$dark}
        overlap={true}
      /> -->

    <div class="main-select-wrapper">
      <div class="select-wrapper">
        <label for="institute-select" class="select-title" class:dark={$dark}
          >Institute/Office</label
        >
        <select
          class="institutes"
          on:change={(event) => {
            othersRev = event?.target.value === "others" ? true : false;
            if (othersRev) {
              newUser.institute = "";
            }

            newUser.institute = event?.target.value;
          }}
          name="institutes"
          id="institute-select"
        >
          <option value="">Select an Option</option>
          <option value="fcdset">FCDSET</option>
          <option value="fnahs">FNAHS</option>
          <option value="false">FALS</option>
          <option value="fted">FTED</option>
          <option value="fcdset">FCDSET</option>
          <option value="fgbm">FGBM</option>
          <option value="others">Others: Please Specify</option>
        </select>
        {#if othersRev}
          <div class="others-wrapper">
            <Input
              inputType="text"
              inputName="N/A if None"
              verifiedEntry={instituteVerified}
              on:input={handleInput}
              bind:focusedInput={inputBinds.otherInput}
              dark={$dark}
              overlap={true}
            />
          </div>
        {/if}
      </div>
      <div class="select-wrapper">
        <label for="institute-select" class="select-title" class:dark={$dark}
          >Designation</label
        >
        <select
          class="institutes"
          on:change={(event) => {
            newUser.unit = event?.target.value;
          }}
          name="institutes"
          id="institute-select"
        >
          <option value="">Select an Option</option>
          <option value="Program Head">Program Head</option>
          <option value="Dean Office">Dean Office</option>
          <option value="Academic VP">Academic VP</option>
          <!-- <option value="Secretary">Secretary</option> -->
          <option value="OP">OP</option>

          <!-- <option value="HROS">HROS</option> -->
          <!-- <option value="VPAA">VPAA</option> -->
        </select>
      </div>
    </div>

    <div class="section-container">
      <CheckBox
        disabled={checkValue ? true : !allVerified}
        checked={checkValue}
        checkboxName="I am not a robot"
        on:change={handleCaptcha}
      />
      <Link to="/auth/reset"><span>forgot password?</span></Link>
    </div>
    <div class="button-container">
      <div class="button">
        <Button hoverized={true} disabled={!checkValue}>Submit</Button>
      </div>
    </div>
    <p class="login-link" class:dark={$dark}>
      Already have an Account?
      <Link to="/auth/login">
        <span>Login</span>
      </Link>
    </p>
  </form>
</main>

<style>
  main {
    display: flex;
    align-items: center;
    justify-content: center;
    column-gap: 2rem;
    margin: 0 3rem;
    height: 90vh;
    position: relative;

    & div.cropper-wrapper {
      display: inline-block;
      width: 18rem;
      height: 18rem;
      margin-top: 1.5rem;
      margin-bottom: 0.5rem;
      position: relative;

      & img.final-user-picture {
        width: 18rem;
        height: 18rem;
        border-radius: 50%;
      }

      & img.user-icon-wrapper {
        width: 18rem;
        height: 18rem;
      }
    }

    & h3 {
      margin-bottom: 0.5rem;
      text-align: center;
      color: var(--main-col-3);
      transition: all ease-in-out 500ms;
    }

    & h3.dark {
      color: var(--background);
    }

    & div.image-wrapper {
      text-align: center;
    }

    & form {
      max-width: 30rem;
      width: 100%;

      & h1 {
        font-size: 2.5rem;
        font-weight: bold;
        letter-spacing: -0.12rem;
        color: var(--main-col-3);
        margin-bottom: 2rem;
      }

      & h1.dark {
        color: var(--background);
      }

      & input[type="file"] {
        display: none;
      }

      & div.input-center-wrapper {
        display: flex;
        column-gap: 1rem;
      }

      & div.main-select-wrapper {
        display: flex;
        align-items: start;
        column-gap: 1rem;

        & div.select-wrapper {
          width: 50%;
          margin-top: 1rem;
          display: flex;
          justify-content: center;
          align-items: center;
          flex-direction: column;
          row-gap: 1rem;
          border: 1px solid var(--main-col-2);
          border-radius: 1rem;
          position: relative;
          padding: 1.5rem 0.5rem 0.5rem 0.5rem;

          & label.select-title {
            position: absolute;
            top: -1.5rem;
            left: 1rem;
            font-size: 1.2rem;
            font-weight: bold;
            padding: 0.5rem;
            background-color: var(--background);
            color: var(--scroll-color);
            transition: all 300ms;
            cursor: pointer;
          }

          & label.dark {
            background-color: var(--dark-main-col-3);
            color: var(--main-col-7);
          }

          & select.institutes {
            width: 100%;
            background-color: var(--background);
            border-radius: 0.5rem;
            padding: 0.5rem;
            border: 1px solid var(--main-col-2);
            font-size: 1.1rem;
            color: var(--scroll-color);
            cursor: pointer;

            & option {
              font-size: 1rem;
            }
          }

          & div.others-wrapper {
            width: 100%;
          }

          & div.others-wrapper > * {
            font-size: 1rem;
          }
        }
      }

      & div.section-container {
        display: flex;
        justify-content: space-between;
        margin: 1.7rem 0;

        & span {
          text-decoration: none;
          color: var(--border-hover-color);
          transition: all ease-in-out 200ms;
        }

        & span:hover {
          opacity: 0.6;
          text-decoration: underline;
        }
      }

      & div.button-container {
        display: flex;

        & div.button {
          width: 8rem;
        }
      }

      & p.login-link {
        margin: 1rem 0;
        color: var(--scroll-color);

        & span {
          text-decoration: none;
          color: var(--border-hover-color);
          transition: all ease-in-out 200ms;
        }

        & span:hover {
          opacity: 0.6;
          text-decoration: underline;
        }
      }

      & p.dark {
        color: var(--header-color);
      }
    }
  }

  @media (max-width: 700px) {
    main {
      margin: 0 2rem;
    }

    main form {
      text-align: center;
    }

    main form div.button-container {
      justify-content: center;
    }
  }

  @media (max-height: 600px) {
    main {
      margin: 7rem 0;
      text-align: center;
    }

    /* img.signup-banner {
      display: none;
    } */

    main form div.button-container {
      justify-content: center;
    }
  }

  @media (max-width: 300px) {
    main {
      margin: 0 1rem;
    }

    main form div.section-container {
      flex-direction: column;
      align-items: center;
      row-gap: 1rem;
    }
  }
</style>
