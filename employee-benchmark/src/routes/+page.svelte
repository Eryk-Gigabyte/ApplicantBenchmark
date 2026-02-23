<script lang="ts">
	import { goto } from '$app/navigation';
	import { submitApplications } from '$lib/postAiAndFile';

	let selectedAIs: string[] = [];
	let isSubmitting = false;

	function toggleAI(name: string, checked: boolean) {
		if (checked) {
			selectedAIs = [...selectedAIs, name];
		} else {
			selectedAIs = selectedAIs.filter((n) => n !== name);
		}
	}

	async function handleSubmit(event: Event) {
		event.preventDefault();

		if (selectedAIs.length === 0) return;

		isSubmitting = true;

		// const result = await submitApplications({
		// 	selectedAIs
		// });

		const result: { success: boolean; redirectUrl?: string; message?: string } = {
			success: true,
			redirectUrl: '/application-compare'
		};

		isSubmitting = false;

		if (result.success) {
			goto(result.redirectUrl || '/application-compare');
		} else {
			alert(result.message || 'Fehler beim Absenden');
		}
	}

	let aiIcons: Array<{ name: string; src: string }> = [];
	try {
		// @ts-ignore
		const modules = import.meta.glob('/src/lib/assets/ai-icons/*.{png,svg,jpg}', { eager: true, as: 'url' });
		aiIcons = Object.keys(modules).map((p) => {
			const file = p.split('/').pop() || p;
			return {
				name: file.replace(/\.(png|svg|jpg)$/i, '').replace(/[-_]/g, ' '),
				// @ts-ignore
				src: modules[p]
			};
		});
	} catch {
		aiIcons = [
			{ name: 'ChatGPT', src: '/src/lib/assets/ai-icons/openai.svg' },
			{ name: 'Gemini', src: '/src/lib/assets/ai-icons/gemini.svg' },
			{ name: 'Claude', src: '/src/lib/assets/ai-icons/claude.svg' },
			{ name: 'DeepSeek', src: '/src/lib/assets/ai-icons/deepseek.svg' }
		];
	}
</script>


<div class="w-full min-h-screen flex items-center justify-center px-4">
	<!-- central content -->
	<div class="max-w-4xl mx-auto">
		<section class="relative z-20 rounded-2xl border border-white/25 p-10 pt-20 pb-20 md:p-22 md:pt-22 md:pb-22 lg:p-30 lg:pt-20 lg:pb-20 backdrop-blur-sm bg-white/05">
			<h1 class="text-center text-3xl md:text-3xl lg:text-4xl font-bold leading-tight md:leading-snug tracking-tight">
				Wer soll deine Bewerber
				<br />
				strukturieren?
			</h1>

			<p class="mt-6 text-m text-left text-white/80">Wähle hier deine AI zum Vergleich aus:</p>
			<p class="mt-1 text-sm text-left text-white/80">(maximal 2 AI's)</p>

			<div class="mt-3">
                <form onsubmit={handleSubmit}>
                    <div class="mt-4 rounded-lg border border-white/30 p-6 flex gap-4 items-center justify-center flex-wrap">
                        {#each aiIcons as icon}
                            <label class="inline-flex gap-3 px-6 py-3 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-white hover:bg-white/15 hover:border-white/30 transition-all duration-200 shadow-lg cursor-pointer has-[:checked]:bg-white/20 has-[:checked]:border-white/40">
                                <input
                                    type="checkbox"
                                    name="selectedAIs"
                                    value={icon.name}
                                    class="appearance-none w-4 h-4 rounded border border-white/30 bg-transparent checked:bg-[url('data:image/svg+xml,%3csvg viewBox=%270 0 16 16%27 fill=%27white%27 xmlns=%27http://www.w3.org/2000/svg%27%3e%3cpath d=%27M12.207 4.793a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0l-2-2a1 1 0 011.414-1.414L6.5 9.086l4.293-4.293a1 1 0 011.414 0z%27/%3e%3c/svg%3e')] checked:bg-center checked:bg-no-repeat"
                                    onchange={(e) => toggleAI(icon.name, e.currentTarget.checked)}
                                />
                                <img src={icon.src} alt={icon.name} class="w-5 h-5 object-contain" />
                                <span class="text-sm font-medium">{icon.name}</span>
                            </label>
                        {/each}
                    </div>

                    <div class="mt-8 flex justify-center">
						<button
							type="submit"
							disabled={selectedAIs.length === 0 || isSubmitting}
							class="px-8 py-3 rounded-full font-semibold transition-all
								{selectedAIs.length === 0 || isSubmitting
									? 'bg-white/10 text-white/40 cursor-not-allowed'
									: 'bg-white text-black hover:bg-white/90'}">
							{isSubmitting ? 'Laden...' : 'Weiter'}
						</button>
                    </div>
                </form>
			</div>
		</section>
	</div>
</div>



