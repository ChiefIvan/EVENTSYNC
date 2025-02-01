<script>
  import { onMount } from "svelte";
  import { fly } from "svelte/transition";
  import { quintOut } from "svelte/easing";
  import { Html5Qrcode } from "html5-qrcode";

  let isScanningDataHasValues = $state(false);
  let isLoading = $state(false);
  let scanning = $state(false);
  let isWarning = $state(true);
  let showPopup = $state(false);
  let scanner = $state(null);
  let msg = $state("");
  let timeOut;

  let scanningData = $state({ id: "", name: "", token: "" });

  const addr = "https://chiefban.pythonanywhere.com/views/register_user";
  const { error, log } = console;

  onMount(() => {
    scanner = new Html5Qrcode("reader");

    scanningData.id = localStorage.getItem("id") || "";
    scanningData.name = localStorage.getItem("name") || "";
    scanningData.token = localStorage.getItem("token") || "";

    Object.values(scanningData).forEach((value) => {
      if (!value.length) {
        isScanningDataHasValues = false;
        return;
      }

      isScanningDataHasValues = true;
    });

    const URLParams = new URLSearchParams(window.location.search);
    const params = ["id", "name", "token"];

    params.forEach((param) => {
      if (!URLParams.has(param) && isScanningDataHasValues) {
        return;
      }

      scanningData[param] = URLParams.get(param);
      localStorage.setItem(param, scanningData[param]);
      URLParams.delete(param);
    });

    window.history.replaceState(
      {},
      "",
      `${window.location.pathname}${URLParams.toString()}`
    );
  });

  const handleModal = (e) => {
    clearTimeout(timeOut);

    showPopup = true;

    timeOut = setTimeout(() => {
      showPopup = false;
    }, 5000);
  };

  const handleSubmit = async (codeData) => {
    isLoading = true;

    try {
      const request = await fetch(addr, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${scanningData.token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          code: codeData,
          id: scanningData.id,
        }),
      });

      const response = await request.json();

      if (request.ok) {
        msg = "Attendance marked successfully.";
        isWarning = false;
        handleModal();
      } else {
        msg = response.msg;
        handleModal();
      }
    } catch (err) {
      msg = "Server unreachable, please try again!";
      handleModal();
      error(err);
    } finally {
      isLoading = false;
      isWarning = true;
    }
  };

  const handleStart = () => {
    scanner.start(
      { facingMode: "environment" },
      {
        fps: 10,
        qrbox: { width: 250, height: 250 },
      },
      onScanSuccess,
      onScanFailure
    );

    scanning = true;
  };

  async function handleStop() {
    await scanner.stop();
    scanning = false;
  }

  const onScanSuccess = async (decodedText, decodedResult) => {
    await handleSubmit(decodedText);
  };

  const onScanFailure = (error) => {
    console.warn(`Code scan error = ${error}`);
  };
</script>

{#if showPopup}
  <div
    class="popup-wrapper"
    transition:fly={{ y: -100, delay: 200, duration: 500, easing: quintOut }}
  >
    <div class="popup">
      <div class="icon-wrapper">
        {#if isWarning}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="50"
            height="50"
            viewBox="0 0 256 256"
            ><path
              fill="orangered"
              d="M236.8 188.09L149.35 36.22a24.76 24.76 0 0 0-42.7 0L19.2 188.09a23.51 23.51 0 0 0 0 23.72A24.35 24.35 0 0 0 40.55 224h174.9a24.35 24.35 0 0 0 21.33-12.19a23.51 23.51 0 0 0 .02-23.72M120 104a8 8 0 0 1 16 0v40a8 8 0 0 1-16 0Zm8 88a12 12 0 1 1 12-12a12 12 0 0 1-12 12"
            /></svg
          >
        {:else}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="60"
            height="60"
            viewBox="0 0 18 18"
            ><path
              fill="#3890f4"
              d="m10.5 13.4l4.9-4.9q.275-.275.7-.275t.7.275q.275.275.275.7t-.275.7l-5.6 5.6q-.3.3-.7.3t-.7-.3l-2.6-2.6q-.275-.275-.275-.7t.275-.7q.275-.275.7-.275t.7.275l1.9 1.9Z"
            /></svg
          >
        {/if}
      </div>
      <h2>EventSync says</h2>
      <p>{msg}</p>
    </div>
  </div>
{/if}

{#if isLoading}
  <div class="spinner-wrapper">
    <svg class="spinner" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
      ><g stroke="#3890f4"
        ><circle
          cx="12"
          cy="12"
          r="9.5"
          fill="none"
          stroke-linecap="round"
          stroke-width="3"
          ><animate
            attributeName="stroke-dasharray"
            calcMode="spline"
            dur="1.5s"
            keySplines="0.42,0,0.58,1;0.42,0,0.58,1;0.42,0,0.58,1"
            keyTimes="0;0.475;0.95;1"
            repeatCount="indefinite"
            values="0 150;42 150;42 150;42 150"
          /><animate
            attributeName="stroke-dashoffset"
            calcMode="spline"
            dur="1.5s"
            keySplines="0.42,0,0.58,1;0.42,0,0.58,1;0.42,0,0.58,1"
            keyTimes="0;0.475;0.95;1"
            repeatCount="indefinite"
            values="0;-16;-59;-59"
          /></circle
        ><animateTransform
          attributeName="transform"
          dur="2s"
          repeatCount="indefinite"
          type="rotate"
          values="0 12 12;360 12 12"
        /></g
      ></svg
    >
  </div>
{/if}

<div id="reader"></div>
<h1>{scanningData.name}</h1>

<div class="button-wrapper">
  {#if scanning}
    <button class="danger" onclick={handleStop}> Stop Scanning</button>
  {:else}
    <button class="primary" onclick={handleStart}> Start Scanning</button>
  {/if}
</div>

<style>
  *,
  *::before,
  *::after {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
    font-size: 1.2rem;
    scrollbar-width: thin;
    font-family: "Poppins", Arial, Helvetica, sans-serif;
  }

  div.popup-wrapper {
    position: absolute;
    top: 0.5rem;
    left: 0;
    right: 0;
    z-index: 10;
    display: flex;
    justify-content: center;

    & div.popup {
      padding-inline: 2rem;
      padding-block: 1rem;
      background-color: #f7d4d4;
      box-shadow: 1px 2px 10px rgba(0, 0, 0, 0.1);
      border-radius: 0.5rem;
      text-align: center;
      max-width: 500px;

      & div.icon-wrapper {
        border-bottom: 1px solid #8d8d8d;
      }

      & h2 {
        margin-top: 1rem;
        font-size: 1.5rem;
        font-weight: 900;
      }

      & p {
        font-weight: 600;
      }
    }
  }

  h1 {
    font-size: 2.5rem;
    display: flex;
    justify-content: center;
    margin: 1rem 0;
  }

  div.spinner-wrapper {
    position: fixed;
    inset: 0;
    z-index: 9999;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.7);

    svg.spinner {
      max-width: 4rem;
      min-width: 3rem;
    }
  }

  div.button-wrapper {
    display: flex;
    justify-content: center;

    button {
      padding: 0.3rem;
      background-color: transparent;
      border-radius: 0.5rem;
      display: flex;
      justify-content: center;
      align-items: center;
      outline-color: #3d4864;
      transition: background 300ms;
      color: #fff;
      width: 100%;
      max-width: 15rem;
    }

    button:hover {
      cursor: pointer;
    }

    button.primary {
      background-color: #0053bd;
      border-color: transparent;
    }

    button.primary:hover {
      background-color: #0a5cff;
    }

    button.primary:active {
      background-color: #3890f4;
    }

    button.danger {
      background-color: #ff0000;
      border-color: transparent;
    }

    button.danger:hover {
      background-color: #fe7a7a;
      border-color: transparent;
    }

    button.danger:active {
      background-color: #fa9393;
    }
  }
</style>
