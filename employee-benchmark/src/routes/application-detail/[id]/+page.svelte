<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/state'; 
    import { ApplicantService } from '$lib/services/applicant';
    import type { Applicant } from '$lib/types/index';

    let applicant = $state<Applicant | null>(null);
    let isLoading = $state(true);
    let error = $state<string | null>(null);

    // Der Parameter aus der URL
    const applicantId = page.params.id;

    onMount(async () => {
        // FIX: Sicherstellen, dass applicantId ein string ist
        if (!applicantId) {
            error = "Keine gültige Bewerber-ID gefunden.";
            isLoading = false;
            return;
        }

        try {
            isLoading = true;
            // Jetzt weiß TypeScript, dass applicantId ein string ist
            applicant = await ApplicantService.getById(applicantId);
        } catch (err) {
            error = "Bewerber konnte nicht geladen werden.";
            console.error(err);
        } finally {
            isLoading = false;
        }
    });
</script>

<div class="p-8 max-w-5xl mx-auto text-white">
    <div class="flex items-center justify-between mb-8">
        <button onclick={() => history.back()} class="text-white/60 hover:text-white transition-colors">
            ← Zurück
        </button>
        {#if applicant}
            <div class="text-right">
                <span class="text-xs text-white/40 block">Modell: {applicant.model_name}</span>
                <span class="text-xs text-white/40 block">Extrahiert am: {new Date(applicant.extracted_at).toLocaleDateString()}</span>
            </div>
        {/if}
    </div>

    {#if isLoading}
        <div class="animate-pulse flex flex-col gap-4">
            <div class="h-12 bg-white/10 rounded w-1/3"></div>
            <div class="h-32 bg-white/10 rounded"></div>
        </div>
    {:else if error}
        <div class="p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-200">{error}</div>
    {:else if applicant}
        <section class="mb-10">
            <h1 class="text-4xl font-bold mb-2">{applicant.name} {applicant.surname}</h1>
            <p class="text-white/60">{applicant.mail} | {applicant.mobile_number ?? 'Keine Nummer'}</p>
        </section>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="bg-white/05 border border-white/10 p-6 rounded-2xl">
                <h2 class="text-xl font-semibold mb-4 text-blue-400">Bildungsweg</h2>
                {#each applicant.education || [] as edu}
                    <div class="mb-4 last:mb-0 border-l-2 border-white/10 pl-4">
                        <p class="font-medium">{edu.school}</p>
                        <p class="text-sm text-white/60">{edu.graduation} ({edu.graduation_grade})</p>
                        <p class="text-xs text-white/40">{edu.begin_date} - {edu.end_date}</p>
                    </div>
                {/each}
            </div>

            <div class="bg-white/05 border border-white/10 p-6 rounded-2xl">
                <h2 class="text-xl font-semibold mb-4 text-purple-400">Berufserfahrung</h2>
                {#each applicant.career || [] as job}
                    <div class="mb-4 last:mb-0 border-l-2 border-white/10 pl-4">
                        <p class="font-medium">{job.employer}</p>
                        <p class="text-sm text-white/80">{job.job_description}</p>
                        <p class="text-xs text-white/40">{job.begin_date} - {job.end_date}</p>
                    </div>
                {/each}
            </div>
        </div>

        <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-8">
             <div class="bg-white/05 border border-white/10 p-6 rounded-2xl">
                <h2 class="text-xl font-semibold mb-4 text-green-400">Qualifikationen</h2>
                <div class="flex flex-wrap gap-2">
                    {#each applicant.qualifications || [] as qual}
                        <span class="bg-white/10 px-3 py-1 rounded-full text-sm">{qual.qualification}</span>
                    {/each}
                </div>
            </div>

            <div class="bg-white/05 border border-white/10 p-6 rounded-2xl">
                <h2 class="text-xl font-semibold mb-4 text-yellow-400">Interessen</h2>
                <p class="text-sm text-white/80"><span class="text-white/40">Hobbies:</span> {applicant.interests?.hobbies ?? 'N/A'}</p>
                <p class="text-sm text-white/80"><span class="text-white/40">Sport:</span> {applicant.interests?.sports ?? 'N/A'}</p>
            </div>
        </div>
    {/if}
</div>