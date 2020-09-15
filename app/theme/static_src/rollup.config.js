import svelte from 'rollup-plugin-svelte';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import livereload from 'rollup-plugin-livereload';
import { terser } from 'rollup-plugin-terser';
import sveltePreprocess from 'svelte-preprocess';
import typescript from '@rollup/plugin-typescript';
import babel from '@rollup/plugin-babel';

const production = !process.env.ROLLUP_WATCH;

const plugins = [
	svelte({
		// enable run-time checks when not in production
		dev: !production,
		// we'll extract any component CSS out into
		// a separate file - better for performance
		css: (css) => {
			css.write('../static/css/svelte.css');
		},
		preprocess: sveltePreprocess(),
	}),

	// If you have external dependencies installed from
	// npm, you'll most likely need these plugins. In
	// some cases you'll need additional configuration -
	// consult the documentation for details:
	// https://github.com/rollup/plugins/tree/master/packages/commonjs
	resolve({
		browser: true,
		dedupe: ['svelte'],
	}),
	commonjs(),
	typescript({ sourceMap: !production }),
	babel({
		exclude: 'node_modules/**',
		babelHelpers: 'bundled',
	}),

	// In dev mode, call `npm run start` once
	// the bundle has been generated
	// !production && serve(),

	// Watch the `public` directory and refresh the
	// browser on changes when not in production
	!production && livereload('../static/js'),

	// If we're building for production (npm run build
	// instead of npm run dev), minify
	production && terser(),
];

const fileNames = [
	'svelte',
	'carousel',
	'drag',
	'http',
	'index',
	'about',
	'infiniteScroll',
	'navbar',
	'register',
	'search',
	'utils',
	'model',
];

export default fileNames.map((name) => {
	const config = {
		output: {
			sourcemap: !production,
			format: 'iife',
			file: `../static/js/${name}.bundle.js`,
			name: name.split('.')[0],
		},
		plugins: [...plugins],
		watch: {
			clearScreen: false,
		},
	};

	if (name === 'svelte') {
		config['input'] = `src/svelte/main.ts`;
	} else if (name === 'model') {
		config['input'] = `src/main/model/index.ts`;
	} else {
		config['input'] = `src/main/${name}.ts`;
	}

	return config;
});
