// noinspection DuplicatedCode

import {codeToHtml} from 'https://esm.sh/shiki'
import MarkdownItAsync from 'https://esm.sh/markdown-it-async'
import {fromAsyncCodeToHtml} from 'https://esm.sh/@shikijs/markdown-it/async'

let md

export async function InitMarkdownRender(displayElement, hiddenElement) {
    md = MarkdownItAsync()
    md.use(fromAsyncCodeToHtml(codeToHtml, {
        themes: {
            dark: 'dracula',
            light: 'vitesse-light'
        },
        defaultColor: 'dark',
    }))
    await RenderMarkdown(displayElement, hiddenElement)
}

async function RenderMarkdown(displayElement, hiddenElement) {
    const markdown = hiddenElement.innerText
    displayElement.innerHTML = await md.renderAsync(markdown)
}