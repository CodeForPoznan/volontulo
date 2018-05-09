/**
 * Util functions for javascript Objects
 */


/**
 * Util function for deep freeze of the object. Utilizes
 * Object.freeze() recursively on all object own enumerable properties
 * @param obj
 */
export function deepFreeze<T>(obj: T): T {
  for (const prop of Object.keys(obj)) {
    if (obj[prop] !== null // 'null' is also of type 'object'
      && (typeof obj[prop] === 'object' || typeof obj[prop] === 'function')
      && !Object.isFrozen(obj[prop])) {
      deepFreeze(obj[prop]);
    }
  }

  return Object.freeze(obj);
}
