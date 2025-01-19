<script>
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";
  import { Html5Qrcode } from "html5-qrcode";

  let isScanningDataHasValues = $state(false);
  let isLoading = $state(false);
  let scanning = $state(false);
  let scanner = $state(null);

  let scanningData = $state({ id: "", name: "", token: "" });

  const addr = "http://127.0.0.1:5000/views/register_user";
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
        alert("Attendance marked successfully.");
      } else {
        // alert(response.msg);
      }
    } catch (err) {
      // alert("Server Unreachable, please try again!");
      error(err);
    } finally {
      isLoading = false;
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
    alert(decodedText);
    await handleSubmit(decodedText);
    console.log(decodedResult);
  };

  const onScanFailure = (error) => {
    console.warn(`Code scan error = ${error}`);
  };
</script>

<div id="reader"></div>
<h1>{scanningData.name}</h1>

{#if isLoading}
  <div class="bar-wrapper">
    <div transition:fade class="bar"></div>
  </div>
{/if}

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

  h1 {
    font-size: 2.5rem;
    display: flex;
    justify-content: center;
    margin: 1rem 0;
  }

  div.bar-wrapper {
    position: fixed;
    inset: 0;
    z-index: 9999;

    div.bar {
      top: 0;
      left: 0;
      right: 0;
      position: absolute;
      width: 100%;
      height: 4px;
      background: var(--light-theme-color-2);
      transition: ease-in-out 500ms;
      overflow: hidden;
    }

    div.bar::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      width: 50%;
      background-color: #0053bd;
      animation: progress 1200ms linear infinite;
    }

    @keyframes progress {
      0% {
        left: -50%;
      }
      50% {
        width: 90%;
      }
      100% {
        left: 120%;
      }
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
