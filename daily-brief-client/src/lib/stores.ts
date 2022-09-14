import { localStore } from '$lib/localStore.js'

const currentTime = localStore('currentTime', null)
const seenPosts = localStore('seenPosts', {})

function reset() {
  currentTime.set(null);
  seenPosts.set({});
}

export {
  currentTime,
  seenPosts,
  reset
}
