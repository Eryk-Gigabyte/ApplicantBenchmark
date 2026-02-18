<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import planet from '$lib/assets/planet.png';
	import rocket from '$lib/assets/rocketship.png';

	let { children } = $props();

	let container: HTMLElement | null = null;
	let planetTransform = 'translate3d(0,0,0)';
	let rocketTransform = 'translate3d(0,0,0)';

	function onPointerMove(e: PointerEvent) {
		if (!container) return;
		const rect = container.getBoundingClientRect();
		const nx = (e.clientX - rect.left) / rect.width - 0.5;
		const ny = (e.clientY - rect.top) / rect.height - 0.5;

		planetTransform = `translate3d(${nx * -30}px, ${ny * -18}px, 0) rotate(${nx * 6}deg)`;
		rocketTransform = `translate3d(${nx * 40}px, ${ny * 26}px, 0) rotate(${nx * -8}deg)`;
	}

	function onPointerLeave() {
		planetTransform = 'translate3d(0,0,0)';
		rocketTransform = 'translate3d(0,0,0)';
	}
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous">
  <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
</svelte:head>


<div bind:this={container} onpointermove={onPointerMove} onpointerleave={onPointerLeave} class="fixed inset-0 z-0">
  <!-- decorative images -->
  <img src={planet} alt="planet" class="pointer-events-none absolute -top-6 -left-6 w-[520px] md:w-[640px] max-w-none opacity-95 drop-shadow-2xl" style="transform: {planetTransform}; transition: transform 180ms linear;" />
  <img src={rocket} alt="rocket" class="pointer-events-none absolute right-[-4rem] bottom-[-2rem] w-[680px] md:w-[920px] max-w-none opacity-95 drop-shadow-2xl" style="transform: {rocketTransform}; transition: transform 180ms linear;" />
</div>

<main class="relative z-10 min-h-screen overflow-auto flex items-start justify-center pointer-events-none">
  <div class="pointer-events-auto">
    {@render children()}
  </div>
</main>

<style lang="postcss">
  @reference "tailwindcss";
  :global(html, body, #svelte) {
    height: 100%;
  }
  :global(body) {
    margin: 0;
    min-height: 100vh;
    overflow: auto;
    background-color: #17191d;
    color: #fff;
    font-family: 'Roboto Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, 'Courier New', monospace;
  }

  :global(body)::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url('../lib/assets/galaxy.jpg');
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center center;
    filter: saturate(1.05) contrast(0.9) brightness(0.55);
    z-index: -1;
    transform: translateZ(0);
  }

  :global(body)::after {
    content: '';
    position: fixed;
    inset: 0;
    background: linear-gradient(180deg, rgba(0,0,0,0.25), rgba(0,0,0,0.45));
    z-index: 0;
    pointer-events: none;
  }
</style>