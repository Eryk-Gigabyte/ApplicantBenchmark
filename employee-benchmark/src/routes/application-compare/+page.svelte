<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import ApplicationsListCard from '$lib/components/ApplicationsListCard.svelte';
    import { ApplicantService } from '$lib/services/applicant';
    import type { Applicant, ProviderBlock } from '$lib/types/index';

    // Filter-Definitionen (Sichtbare Spalten)
    const filterTypes: string[] = ['name', 'surname', 'mail', 'applicant_id'];
    let activeFilters = $state<string[]>([...filterTypes]);

    // Zustand für die dynamischen Daten
    let providers = $state<ProviderBlock[]>([]);
    let isLoading = $state(true);
    let error = $state<string | null>(null);

    // Mapping von Modellnamen (aus DB) zu deinen lokalen Icons
    const iconMap: Record<string, string> = {
        'gpt-4': '/src/lib/assets/ai-icons/openai.svg',
        'gpt-4o': '/src/lib/assets/ai-icons/openai.svg',
        'deepseek-v3': '/src/lib/assets/ai-icons/deepseek.svg',
        'gemini-1.5': '/src/lib/assets/ai-icons/gemini.svg',
        'claude-3': '/src/lib/assets/ai-icons/claude.svg'
    };

    function toggleFilter(f: string) {
        if (activeFilters.includes(f)) {
            activeFilters = activeFilters.filter((x) => x !== f);
        } else {
            activeFilters = [...activeFilters, f];
        }
    }

    onMount(async () => {
        try {
            isLoading = true;
            // 1. Daten vom Backend laden
            const allApplicants = await ApplicantService.getOverview();

            // 2. Gruppierung der flachen Liste in das ProviderBlock-Format
            const grouped = allApplicants.reduce((acc, app) => {
                const model = app.model_name || 'Unbekannt';
                
                if (!acc[model]) {
                    acc[model] = {
                        provider: { 
                            name: model, 
                            icon: iconMap[model] || '/src/lib/assets/ai-icons/openai.svg' // Fallback
                        },
                        metadata: { answerTime: 0, tokens: 0 }, // Platzhalter (oder aus LLM_Logs laden)
                        applications: []
                    };
                }
                acc[model].applications.push(app);
                return acc;
            }, {} as Record<string, ProviderBlock>);

            providers = Object.values(grouped);
        } catch (err) {
            error = "Verbindung zum Backend fehlgeschlagen.";
            console.error(err);
        } finally {
            isLoading = false;
        }
    });
</script>

<div class="p-6 w-[90vw] max-w-none mx-auto">
    <button
        onclick={() => goto('/')}
        class="text-sm text-white/80 bg-transparent px-3 py-1 rounded hover:bg-white/10 border border-white/10 transition-colors"
        aria-label="Zurück zur Startseite"
    >
        ← Zurück
    </button>

    <div class="mt-6 mb-4 flex items-center justify-between">
        <h1 class="text-3xl font-bold mb-0 text-white">Bewerber Vergleich</h1>
    </div>

    <div class="relative z-50 sticky top-6 pointer-events-auto rounded-xl p-4 mb-6 bg-white/05 backdrop-blur-md border border-white/20">
        <div class="text-sm text-white/80 font-medium mb-3">Sichtbare Spalten</div>
        <div class="flex gap-3 items-center flex-wrap">
            <div class="flex gap-2 flex-wrap">
                {#each filterTypes as f}
                    <button
                        onclick={() => toggleFilter(f)}
                        class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm transition-all
                        {activeFilters.includes(f) 
                            ? 'bg-white/20 border border-white/30 text-white shadow-lg' 
                            : 'bg-transparent border border-white/10 text-white/50 hover:bg-white/05'}"
                    >
                        <span>{f}</span>
                        {#if activeFilters.includes(f)}
                            <span class="ml-1 text-white/60">×</span>
                        {/if}
                    </button>
                {/each}
            </div>
        </div>
    </div>

    {#if isLoading}
        <div class="flex justify-center items-center h-64">
            <div class="text-white/60 animate-pulse text-lg">Lade Benchmarks aus der Datenbank...</div>
        </div>
    {:else if error}
        <div class="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-xl text-center">
            {error}
        </div>
    {:else if providers.length === 0}
        <div class="text-white/40 text-center py-20 border border-dashed border-white/10 rounded-2xl">
            Keine Daten gefunden. Bitte führen Sie zuerst einen Benchmark aus.
        </div>
    {:else}
        <ApplicationsListCard {providers} columns={activeFilters} />
    {/if}
</div>