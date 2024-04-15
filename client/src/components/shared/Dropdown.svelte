<script>
  import { dark } from "../../store";
  export let expand = false;
  export let outside = false;
  export let docs = false;
  export let status = false;
  export let overview = false;
  export let secretary = false;
  export let self = false;
  export let admin = false;
</script>

<div
  class="wrapper"
  class:outside
  class:docs
  class:status
  class:overview
  class:secretary
  class:self
  class:admin
  class:wrapper-expand={expand}
  class:dark={$dark}
>
  <ul class="li-wrapper">
    <slot />
  </ul>
</div>

<style>
  div.wrapper {
    display: grid;
    grid-template-rows: 0fr;

    overflow: hidden;
    position: fixed;
    top: 3.5rem;
    right: 2.5rem;
    z-index: 1;

    transition: all ease-in-out 400ms;
    background-color: var(--background);
    border-radius: 0.5rem;
    box-shadow: 5px 5px 25px rgba(0, 0, 0, 0.3);

    & ul.li-wrapper {
      min-height: 0;
    }
  }

  div.outside {
    right: 0.5rem;
  }

  div.docs {
    position: absolute;
    right: 0;
    left: 0;
  }

  div.status {
    position: absolute;
    top: 2.5rem;
    right: 0;
    width: 6rem;
  }

  div.overview {
    top: 6rem;
    right: 1rem;
    width: 6rem;
  }

  div.secretary {
    position: absolute;
    top: 3.5rem;
    right: 2rem;
    width: 8rem;
  }

  div.self {
    position: absolute;
    top: 3.5rem;
    right: 8.5rem;
    width: 6rem;
  }

  div.admin {
    position: absolute;
    top: 2.5rem;
    right: 0;
    width: 10rem;
  }

  div.wrapper-expand {
    grid-template-rows: 1fr;
  }

  div.dark {
    background-color: var(--dark-main-col-1);
  }
</style>
