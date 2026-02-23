<script lang="ts">
	import ApplicationsListCard from '$lib/components/ApplicationsListCard.svelte';
	import { goto } from '$app/navigation';

	const filterTypes: string[] = ['Name', 'Skills', 'E‑Mail', 'Position'];
	let activeFilters = $state<string[]>([...filterTypes]);

	function toggleFilter(f: string) {
		if (activeFilters.includes(f)) {
			activeFilters = activeFilters.filter((x) => x !== f);
		} else {
			activeFilters = [...activeFilters, f];
		}
	}

	// No free-text search: activeFilters control which columns are visible.

	const providers = [
		{
			provider: { name: 'ChatGPT', icon: '/src/lib/assets/ai-icons/openai.svg' },
			metadata: { answerTime: 15000, tokens: 1 },
			applications: [
				{ name: 'Anna Müller', skills: ['Python','JavaScript','React'], email: 'Anna.Müller@icloud.com', position: 'Senior' },
				{ name: 'Peter Müller', skills: ['Python','JavaScript','React'], email: 'Peter.Mueller@icloud.com', position: 'Junior' },
				{ name: 'Anna Müller', skills: ['Python','JavaScript','React'], email: 'Anna.Müller@icloud.com', position: 'Principal' },
				{ name: 'Anna Müller', skills: ['Python','JavaScript','React'], email: 'Anna.Müller@icloud.com', position: 'trainee' }
			]
		},
		{
			provider: { name: 'DeepSeek', icon: '/src/lib/assets/ai-icons/deepseek.svg' },
			metadata: { answerTime: 15000, tokens: 1 },
			applications: [
				{ name: 'Anna Müller', skills: ['Python','JavaScript','React'], email: 'Anna.Müller@icloud.com', position: 'Senior' },
				{ name: 'Anna Müller', skills: ['Python','JavaScript','React'], email: 'Anna.Müller@icloud.com', position: 'Junior' },
				{ name: 'Anna Müller', skills: ['Python','JavaScript','React'], email: 'Anna.Müller@icloud.com', position: 'Principal' },
				{ name: 'Anna Müller', skills: ['Python','JavaScript','React'], email: 'Anna.Müller@icloud.com', position: 'trainee' }
			]
		},
{
			provider: { name: 'gemini', icon: '/src/lib/assets/ai-icons/gemini.svg' },
			metadata: { answerTime: 15000, tokens: 1 },
			applications: [
				{ name: 'Anna Müller', skills: ['Python','JavaScript','React'], email: 'Anna.Müller@icloud.com', position: 'Senior' },
				{ name: 'Anna Müller', skills: ['Python','JavaScript','React'], email: 'Anna.Müller@icloud.com', position: 'Junior' },
				{ name: 'Anna Müller', skills: ['Python','JavaScript','React'], email: 'Anna.Müller@icloud.com', position: 'Principal' },
				{ name: 'Anna Müller', skills: ['Python','JavaScript','React'], email: 'Anna.Müller@icloud.com', position: 'trainee' }
			]
		}
	];
</script>

<div class="p-6 w-[90vw] max-w-none mx-auto">
    	<button
			onclick={() => goto('/')}
			class="text-sm text-white/80 bg-transparent px-3 py-1 rounded hover:bg-white/03 border border-white/10"
			aria-label="Zurück zur Startseite"
		>
			← Zurück
		</button>
	<div class="mt-6 mb-4 flex items-center justify-between">
		<h1 class="text-3xl font-bold mb-0 text-white">Bewerber</h1>
	</div>

	<!-- Quick Filter UI -->
	<div class="relative z-50 sticky top-6 pointer-events-auto rounded-xl border border-white/25 p-4 mb-6 bg-white/06 backdrop-blur-md border border-white/20">
		<div class="text-sm text-white/80 font-medium mb-3">Schnell Filter</div>
			<div class="flex gap-3 items-center flex-wrap">
				<!-- predefined toggle chips (no search input) -->
				<div class="flex gap-2 flex-wrap">
				{#each filterTypes as f}
					{#if activeFilters.includes(f)}
						<button
							onclick={() => toggleFilter(f)}
							aria-pressed={true}
							class="inline-flex items-center gap-2 bg-white/30 border border-white/10 text-white px-3 py-1 rounded-full text-sm shadow-sm"
							aria-label={`Deselect ${f}`}
						>
							<span>{f}</span>
							<span class="ml-1 text-white/80">×</span>
						</button>
					{:else}
						<button
							onclick={() => toggleFilter(f)}
							aria-pressed={false}
							class="inline-flex items-center gap-2 bg-transparent border border-white/10 text-white/70 px-3 py-1 rounded-full text-sm hover:bg-white/03 focus:outline-none focus:ring-2 focus:ring-white/10"
							aria-label={`Select ${f}`}
						>
							{f}
						</button>
					{/if}
				{/each}
				</div>
			</div>
	</div>
	<ApplicationsListCard providers={providers} columns={activeFilters}/>
</div>


	


