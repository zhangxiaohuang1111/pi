/*!--------------------------------------------------------
 * Copyright (C) Microsoft Corporation. All rights reserved.
 *--------------------------------------------------------*/var v=function(e,r){return v=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,o){t.__proto__=o}||function(t,o){for(var i in o)Object.prototype.hasOwnProperty.call(o,i)&&(t[i]=o[i])},v(e,r)};export function __extends(e,r){if(typeof r!="function"&&r!==null)throw new TypeError("Class extends value "+String(r)+" is not a constructor or null");v(e,r);function t(){this.constructor=e}e.prototype=r===null?Object.create(r):(t.prototype=r.prototype,new t)}export var __assign=function(){return __assign=Object.assign||function(r){for(var t,o=1,i=arguments.length;o<i;o++){t=arguments[o];for(var n in t)Object.prototype.hasOwnProperty.call(t,n)&&(r[n]=t[n])}return r},__assign.apply(this,arguments)};export function __rest(e,r){var t={};for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&r.indexOf(o)<0&&(t[o]=e[o]);if(e!=null&&typeof Object.getOwnPropertySymbols=="function")for(var i=0,o=Object.getOwnPropertySymbols(e);i<o.length;i++)r.indexOf(o[i])<0&&Object.prototype.propertyIsEnumerable.call(e,o[i])&&(t[o[i]]=e[o[i]]);return t}export function __decorate(e,r,t,o){var i=arguments.length,n=i<3?r:o===null?o=Object.getOwnPropertyDescriptor(r,t):o,a;if(typeof Reflect=="object"&&typeof Reflect.decorate=="function")n=Reflect.decorate(e,r,t,o);else for(var f=e.length-1;f>=0;f--)(a=e[f])&&(n=(i<3?a(n):i>3?a(r,t,n):a(r,t))||n);return i>3&&n&&Object.defineProperty(r,t,n),n}export function __param(e,r){return function(t,o){r(t,o,e)}}export function __esDecorate(e,r,t,o,i,n){function a(g){if(g!==void 0&&typeof g!="function")throw new TypeError("Function expected");return g}for(var f=o.kind,c=f==="getter"?"get":f==="setter"?"set":"value",s=!r&&e?o.static?e:e.prototype:null,u=r||(s?Object.getOwnPropertyDescriptor(s,o.name):{}),p,_=!1,l=t.length-1;l>=0;l--){var d={};for(var m in o)d[m]=m==="access"?{}:o[m];for(var m in o.access)d.access[m]=o.access[m];d.addInitializer=function(g){if(_)throw new TypeError("Cannot add initializers after decoration has completed");n.push(a(g||null))};var y=(0,t[l])(f==="accessor"?{get:u.get,set:u.set}:u[c],d);if(f==="accessor"){if(y===void 0)continue;if(y===null||typeof y!="object")throw new TypeError("Object expected");(p=a(y.get))&&(u.get=p),(p=a(y.set))&&(u.set=p),(p=a(y.init))&&i.unshift(p)}else(p=a(y))&&(f==="field"?i.unshift(p):u[c]=p)}s&&Object.defineProperty(s,o.name,u),_=!0}export function __runInitializers(e,r,t){for(var o=arguments.length>2,i=0;i<r.length;i++)t=o?r[i].call(e,t):r[i].call(e);return o?t:void 0}export function __propKey(e){return typeof e=="symbol"?e:"".concat(e)}export function __setFunctionName(e,r,t){return typeof r=="symbol"&&(r=r.description?"[".concat(r.description,"]"):""),Object.defineProperty(e,"name",{configurable:!0,value:t?"".concat(t," ",r):r})}export function __metadata(e,r){if(typeof Reflect=="object"&&typeof Reflect.metadata=="function")return Reflect.metadata(e,r)}export function __awaiter(e,r,t,o){function i(n){return n instanceof t?n:new t(function(a){a(n)})}return new(t||(t=Promise))(function(n,a){function f(u){try{s(o.next(u))}catch(p){a(p)}}function c(u){try{s(o.throw(u))}catch(p){a(p)}}function s(u){u.done?n(u.value):i(u.value).then(f,c)}s((o=o.apply(e,r||[])).next())})}export function __generator(e,r){var t={label:0,sent:function(){if(n[0]&1)throw n[1];return n[1]},trys:[],ops:[]},o,i,n,a;return a={next:f(0),throw:f(1),return:f(2)},typeof Symbol=="function"&&(a[Symbol.iterator]=function(){return this}),a;function f(s){return function(u){return c([s,u])}}function c(s){if(o)throw new TypeError("Generator is already executing.");for(;a&&(a=0,s[0]&&(t=0)),t;)try{if(o=1,i&&(n=s[0]&2?i.return:s[0]?i.throw||((n=i.return)&&n.call(i),0):i.next)&&!(n=n.call(i,s[1])).done)return n;switch(i=0,n&&(s=[s[0]&2,n.value]),s[0]){case 0:case 1:n=s;break;case 4:return t.label++,{value:s[1],done:!1};case 5:t.label++,i=s[1],s=[0];continue;case 7:s=t.ops.pop(),t.trys.pop();continue;default:if(n=t.trys,!(n=n.length>0&&n[n.length-1])&&(s[0]===6||s[0]===2)){t=0;continue}if(s[0]===3&&(!n||s[1]>n[0]&&s[1]<n[3])){t.label=s[1];break}if(s[0]===6&&t.label<n[1]){t.label=n[1],n=s;break}if(n&&t.label<n[2]){t.label=n[2],t.ops.push(s);break}n[2]&&t.ops.pop(),t.trys.pop();continue}s=r.call(e,t)}catch(u){s=[6,u],i=0}finally{o=n=0}if(s[0]&5)throw s[1];return{value:s[0]?s[1]:void 0,done:!0}}}export var __createBinding=Object.create?function(e,r,t,o){o===void 0&&(o=t);var i=Object.getOwnPropertyDescriptor(r,t);(!i||("get"in i?!r.__esModule:i.writable||i.configurable))&&(i={enumerable:!0,get:function(){return r[t]}}),Object.defineProperty(e,o,i)}:function(e,r,t,o){o===void 0&&(o=t),e[o]=r[t]};export function __exportStar(e,r){for(var t in e)t!=="default"&&!Object.prototype.hasOwnProperty.call(r,t)&&__createBinding(r,e,t)}export function __values(e){var r=typeof Symbol=="function"&&Symbol.iterator,t=r&&e[r],o=0;if(t)return t.call(e);if(e&&typeof e.length=="number")return{next:function(){return e&&o>=e.length&&(e=void 0),{value:e&&e[o++],done:!e}}};throw new TypeError(r?"Object is not iterable.":"Symbol.iterator is not defined.")}export function __read(e,r){var t=typeof Symbol=="function"&&e[Symbol.iterator];if(!t)return e;var o=t.call(e),i,n=[],a;try{for(;(r===void 0||r-- >0)&&!(i=o.next()).done;)n.push(i.value)}catch(f){a={error:f}}finally{try{i&&!i.done&&(t=o.return)&&t.call(o)}finally{if(a)throw a.error}}return n}export function __spread(){for(var e=[],r=0;r<arguments.length;r++)e=e.concat(__read(arguments[r]));return e}export function __spreadArrays(){for(var e=0,r=0,t=arguments.length;r<t;r++)e+=arguments[r].length;for(var o=Array(e),i=0,r=0;r<t;r++)for(var n=arguments[r],a=0,f=n.length;a<f;a++,i++)o[i]=n[a];return o}export function __spreadArray(e,r,t){if(t||arguments.length===2)for(var o=0,i=r.length,n;o<i;o++)(n||!(o in r))&&(n||(n=Array.prototype.slice.call(r,0,o)),n[o]=r[o]);return e.concat(n||Array.prototype.slice.call(r))}export function __await(e){return this instanceof __await?(this.v=e,this):new __await(e)}export function __asyncGenerator(e,r,t){if(!Symbol.asyncIterator)throw new TypeError("Symbol.asyncIterator is not defined.");var o=t.apply(e,r||[]),i,n=[];return i={},f("next"),f("throw"),f("return",a),i[Symbol.asyncIterator]=function(){return this},i;function a(l){return function(d){return Promise.resolve(d).then(l,p)}}function f(l,d){o[l]&&(i[l]=function(m){return new Promise(function(y,g){n.push([l,m,y,g])>1||c(l,m)})},d&&(i[l]=d(i[l])))}function c(l,d){try{s(o[l](d))}catch(m){_(n[0][3],m)}}function s(l){l.value instanceof __await?Promise.resolve(l.value.v).then(u,p):_(n[0][2],l)}function u(l){c("next",l)}function p(l){c("throw",l)}function _(l,d){l(d),n.shift(),n.length&&c(n[0][0],n[0][1])}}export function __asyncDelegator(e){var r,t;return r={},o("next"),o("throw",function(i){throw i}),o("return"),r[Symbol.iterator]=function(){return this},r;function o(i,n){r[i]=e[i]?function(a){return(t=!t)?{value:__await(e[i](a)),done:!1}:n?n(a):a}:n}}export function __asyncValues(e){if(!Symbol.asyncIterator)throw new TypeError("Symbol.asyncIterator is not defined.");var r=e[Symbol.asyncIterator],t;return r?r.call(e):(e=typeof __values=="function"?__values(e):e[Symbol.iterator](),t={},o("next"),o("throw"),o("return"),t[Symbol.asyncIterator]=function(){return this},t);function o(n){t[n]=e[n]&&function(a){return new Promise(function(f,c){a=e[n](a),i(f,c,a.done,a.value)})}}function i(n,a,f,c){Promise.resolve(c).then(function(s){n({value:s,done:f})},a)}}export function __makeTemplateObject(e,r){return Object.defineProperty?Object.defineProperty(e,"raw",{value:r}):e.raw=r,e}var j=Object.create?function(e,r){Object.defineProperty(e,"default",{enumerable:!0,value:r})}:function(e,r){e.default=r};export function __importStar(e){if(e&&e.__esModule)return e;var r={};if(e!=null)for(var t in e)t!=="default"&&Object.prototype.hasOwnProperty.call(e,t)&&__createBinding(r,e,t);return j(r,e),r}export function __importDefault(e){return e&&e.__esModule?e:{default:e}}export function __classPrivateFieldGet(e,r,t,o){if(t==="a"&&!o)throw new TypeError("Private accessor was defined without a getter");if(typeof r=="function"?e!==r||!o:!r.has(e))throw new TypeError("Cannot read private member from an object whose class did not declare it");return t==="m"?o:t==="a"?o.call(e):o?o.value:r.get(e)}export function __classPrivateFieldSet(e,r,t,o,i){if(o==="m")throw new TypeError("Private method is not writable");if(o==="a"&&!i)throw new TypeError("Private accessor was defined without a setter");if(typeof r=="function"?e!==r||!i:!r.has(e))throw new TypeError("Cannot write private member to an object whose class did not declare it");return o==="a"?i.call(e,t):i?i.value=t:r.set(e,t),t}export function __classPrivateFieldIn(e,r){if(r===null||typeof r!="object"&&typeof r!="function")throw new TypeError("Cannot use 'in' operator on non-object");return typeof e=="function"?r===e:e.has(r)}export function __addDisposableResource(e,r,t){if(r!=null){if(typeof r!="object"&&typeof r!="function")throw new TypeError("Object expected.");var o,i;if(t){if(!Symbol.asyncDispose)throw new TypeError("Symbol.asyncDispose is not defined.");o=r[Symbol.asyncDispose]}if(o===void 0){if(!Symbol.dispose)throw new TypeError("Symbol.dispose is not defined.");o=r[Symbol.dispose],t&&(i=o)}if(typeof o!="function")throw new TypeError("Object not disposable.");i&&(o=function(){try{i.call(this)}catch(n){return Promise.reject(n)}}),e.stack.push({value:r,dispose:o,async:t})}else t&&e.stack.push({async:!0});return r}var A=typeof SuppressedError=="function"?SuppressedError:function(e,r,t){var o=new Error(t);return o.name="SuppressedError",o.error=e,o.suppressed=r,o};export function __disposeResources(e){function r(o){e.error=e.hasError?new A(o,e.error,"An error was suppressed during disposal."):o,e.hasError=!0}function t(){for(;e.stack.length;){var o=e.stack.pop();try{var i=o.dispose&&o.dispose.call(o.value);if(o.async)return Promise.resolve(i).then(t,function(n){return r(n),t()})}catch(n){r(n)}}if(e.hasError)throw e.error}return t()}export default{__extends,__assign,__rest,__decorate,__param,__metadata,__awaiter,__generator,__createBinding,__exportStar,__values,__read,__spread,__spreadArrays,__spreadArray,__await,__asyncGenerator,__asyncDelegator,__asyncValues,__makeTemplateObject,__importStar,__importDefault,__classPrivateFieldGet,__classPrivateFieldSet,__classPrivateFieldIn,__addDisposableResource,__disposeResources};var O={exports:{}};(function(){function r(n){const a=[];typeof n=="number"&&a.push("code/timeOrigin",n);function f(s){a.push(s,Date.now())}function c(){const s=[];for(let u=0;u<a.length;u+=2)s.push({name:a[u],startTime:a[u+1]});return s}return{mark:f,getMarks:c}}function t(){if(typeof performance=="object"&&typeof performance.mark=="function"&&!performance.nodeTiming)return typeof performance.timeOrigin!="number"&&!performance.timing?r():{mark(n){performance.mark(n)},getMarks(){let n=performance.timeOrigin;typeof n!="number"&&(n=performance.timing.navigationStart||performance.timing.redirectStart||performance.timing.fetchStart);const a=[{name:"code/timeOrigin",startTime:Math.round(n)}];for(const f of performance.getEntriesByType("mark"))a.push({name:f.name,startTime:Math.round(n+f.startTime)});return a}};if(typeof process=="object"){const n=performance?.timeOrigin;return r(n)}else return console.trace("perf-util loaded in UNKNOWN environment"),r()}function o(n){return n.MonacoPerformanceMarks||(n.MonacoPerformanceMarks=t()),n.MonacoPerformanceMarks}var i;typeof global=="object"?i=global:typeof self=="object"?i=self:i={},typeof O=="object"&&typeof O.exports=="object"?O.exports=o(i):(console.trace("perf-util defined in UNKNOWN context (neither requirejs or commonjs)"),i.perf=o(i))})();var S=O.exports.mark,ne=O.exports.getMarks;import*as b from"path";import*as D from"fs";import{fileURLToPath as I}from"url";import{createRequire as L}from"node:module";var N=L(import.meta.url),h={exports:{}},M=b.dirname(I(import.meta.url));if(Error.stackTraceLimit=100,!process.env.VSCODE_HANDLES_SIGPIPE){let e=!1;process.on("SIGPIPE",()=>{e||(e=!0,console.error(new Error("Unexpected SIGPIPE")))})}function U(){try{typeof process.env.VSCODE_CWD!="string"&&(process.env.VSCODE_CWD=process.cwd()),process.platform==="win32"&&process.chdir(b.dirname(process.execPath))}catch(e){console.error(e)}}U(),h.exports.devInjectNodeModuleLookupPath=function(e){if(!process.env.VSCODE_DEV)return;if(!e)throw new Error("Missing injectPath");N("node:module").register("./bootstrap-import.js",{parentURL:import.meta.url,data:e})},h.exports.removeGlobalNodeJsModuleLookupPaths=function(){if(typeof process?.versions?.electron=="string")return;const e=N("module"),r=e.globalPaths,t=e._resolveLookupPaths;e._resolveLookupPaths=function(o,i){const n=t(o,i);if(Array.isArray(n)){let a=0;for(;a<n.length&&n[n.length-1-a]===r[r.length-1-a];)a++;return n.slice(0,n.length-a)}return n}},h.exports.configurePortable=function(e){const r=b.dirname(M);function t(c){return process.env.VSCODE_DEV?r:process.platform==="darwin"?c.dirname(c.dirname(c.dirname(r))):c.dirname(c.dirname(r))}function o(c){if(process.env.VSCODE_PORTABLE)return process.env.VSCODE_PORTABLE;if(process.platform==="win32"||process.platform==="linux")return c.join(t(c),"data");const s=e.portable||`${e.applicationName}-portable-data`;return c.join(c.dirname(t(c)),s)}const i=o(b),n=!("target"in e)&&D.existsSync(i),a=b.join(i,"tmp"),f=n&&D.existsSync(a);return n?process.env.VSCODE_PORTABLE=i:delete process.env.VSCODE_PORTABLE,f&&(process.platform==="win32"?(process.env.TMP=a,process.env.TEMP=a):process.env.TMPDIR=a),{portableDataPath:i,isPortable:n}},h.exports.enableASARSupport=function(){},h.exports.fileUriFromPath=function(e,r){let t=e.replace(/\\/g,"/");t.length>0&&t.charAt(0)!=="/"&&(t=`/${t}`);let o;return r.isWindows&&t.startsWith("//")?o=encodeURI(`${r.scheme||"file"}:${t}`):o=encodeURI(`${r.scheme||"file"}://${r.fallbackAuthority||""}${t}`),o.replace(/#/g,"%23")};var V=h.exports.devInjectNodeModuleLookupPath,G=h.exports.removeGlobalNodeJsModuleLookupPaths,se=h.exports.configurePortable,F=h.exports.enableASARSupport,ce=h.exports.fileUriFromPath;import*as k from"path";import*as w from"fs";import{fileURLToPath as $}from"url";import{createRequire as B,register as J}from"node:module";import{createRequire as q}from"node:module";var R=q(import.meta.url),E={exports:{}},P={BUILD_INSERT_PRODUCT_CONFIGURATION:"BUILD_INSERT_PRODUCT_CONFIGURATION"};P.BUILD_INSERT_PRODUCT_CONFIGURATION&&(P=R("../product.json"));var x={"name":"Code","version":"1.94.0","private":true,"overrides":{"node-gyp-build":"4.8.1"},"type":"module"};x.BUILD_INSERT_PACKAGE_CONFIGURATION&&(x=R("../package.json")),E.exports.product=P,E.exports.pkg=x;var H=E.exports.product,K=E.exports.pkg,W=B(import.meta.url),C={exports:{}},X=k.dirname($(import.meta.url));if((process.env.ELECTRON_RUN_AS_NODE||process.versions.electron)&&J(`data:text/javascript;base64,${Buffer.from(`
	export async function resolve(specifier, context, nextResolve) {
		if (specifier === 'fs') {
			return {
				format: 'builtin',
				shortCircuit: true,
				url: 'node:original-fs'
			};
		}

		// Defer to the next hook in the chain, which would be the
		// Node.js default resolve if this is the last user-specified loader.
		return nextResolve(specifier, context);
	}`).toString("base64")}`,import.meta.url),globalThis._VSCODE_PRODUCT_JSON={...H},process.env.VSCODE_DEV)try{const e=W("../product.overrides.json");globalThis._VSCODE_PRODUCT_JSON=Object.assign(globalThis._VSCODE_PRODUCT_JSON,e)}catch{}globalThis._VSCODE_PACKAGE_JSON={...K},globalThis._VSCODE_FILE_ROOT=X;var T=void 0;function Y(){return T||(T=Q()),T}async function Q(){S("code/amd/willLoadNls");let e,r;if(process.env.VSCODE_NLS_CONFIG)try{e=JSON.parse(process.env.VSCODE_NLS_CONFIG),e?.languagePack?.messagesFile?r=e.languagePack.messagesFile:e?.defaultMessagesFile&&(r=e.defaultMessagesFile),globalThis._VSCODE_NLS_LANGUAGE=e?.resolvedLanguage}catch(t){console.error(`Error reading VSCODE_NLS_CONFIG from environment: ${t}`)}if(!(process.env.VSCODE_DEV||!r)){try{globalThis._VSCODE_NLS_MESSAGES=JSON.parse((await w.promises.readFile(r)).toString())}catch(t){if(console.error(`Error reading NLS messages file ${r}: ${t}`),e?.languagePack?.corruptMarkerFile)try{await w.promises.writeFile(e.languagePack.corruptMarkerFile,"corrupted")}catch(o){console.error(`Error writing corrupted NLS marker file: ${o}`)}if(e?.defaultMessagesFile&&e.defaultMessagesFile!==r)try{globalThis._VSCODE_NLS_MESSAGES=JSON.parse((await w.promises.readFile(e.defaultMessagesFile)).toString())}catch(o){console.error(`Error reading default NLS messages file ${e.defaultMessagesFile}: ${o}`)}}return S("code/amd/didLoadNls"),e}}C.exports.load=function(e,r,t){e&&(e=`./${e}.js`,r=r||function(){},t=t||function(o){console.error(o)},Y().then(()=>{S("code/fork/willLoadCode"),import(e).then(r,t)}))};var z=C.exports.load;S("code/fork/start"),te(),G(),F(),process.env.VSCODE_DEV_INJECT_NODE_MODULE_LOOKUP_PATH&&V(process.env.VSCODE_DEV_INJECT_NODE_MODULE_LOOKUP_PATH),process.send&&process.env.VSCODE_PIPE_LOGGING==="true"&&Z(),process.env.VSCODE_HANDLES_UNCAUGHT_ERRORS||ee(),process.env.VSCODE_PARENT_PID&&re(),z(process.env.VSCODE_AMD_ENTRYPOINT);function Z(){function t(c){const s=[],u=[];if(c.length)for(let p=0;p<c.length;p++){let _=c[p];if(typeof _>"u")_="undefined";else if(_ instanceof Error){const l=_;l.stack?_=l.stack:_=l.toString()}u.push(_)}try{const p=JSON.stringify(u,function(_,l){if(i(l)||Array.isArray(l)){if(s.indexOf(l)!==-1)return"[Circular]";s.push(l)}return l});return p.length>1e5?"Output omitted for a large object that exceeds the limits":p}catch(p){return`Output omitted for an object that cannot be inspected ('${p.toString()}')`}}function o(c){try{process.send&&process.send(c)}catch{}}function i(c){return typeof c=="object"&&c!==null&&!Array.isArray(c)&&!(c instanceof RegExp)&&!(c instanceof Date)}function n(c,s){o({type:"__$console",severity:c,arguments:s})}function a(c,s){Object.defineProperty(console,c,{set:()=>{},get:()=>function(){n(s,t(arguments))}})}function f(c,s){const u=process[c],p=u.write;let _="";Object.defineProperty(u,"write",{set:()=>{},get:()=>(l,d,m)=>{_+=l.toString(d);const y=_.length>1048576?_.length:_.lastIndexOf(`
`);y!==-1&&(console[s](_.slice(0,y)),_=_.slice(y+1)),p.call(u,l,d,m)}})}process.env.VSCODE_VERBOSE_LOGGING==="true"?(a("info","log"),a("log","log"),a("warn","warn"),a("error","error")):(console.log=function(){},console.warn=function(){},console.info=function(){},a("error","error")),f("stderr","error"),f("stdout","log")}function ee(){process.on("uncaughtException",function(e){console.error("Uncaught Exception: ",e)}),process.on("unhandledRejection",function(e){console.error("Unhandled Promise Rejection: ",e)})}function re(){const e=Number(process.env.VSCODE_PARENT_PID);typeof e=="number"&&!isNaN(e)&&setInterval(function(){try{process.kill(e,0)}catch{process.exit()}},5e3)}function te(){const e=process.env.VSCODE_CRASH_REPORTER_PROCESS_TYPE;if(e)try{process.crashReporter&&typeof process.crashReporter.addExtraParameter=="function"&&process.crashReporter.addExtraParameter("processType",e)}catch(r){console.error(r)}}

//# sourceMappingURL=https://main.vscode-cdn.net/sourcemaps/d78a74bcdfad14d5d3b1b782f87255d802b57511/core/bootstrap-fork.js.map