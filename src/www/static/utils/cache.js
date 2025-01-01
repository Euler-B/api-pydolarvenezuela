class Cache {
  constructor(defaultTTL) {
    this.defaultTTL = defaultTTL;
  }

  // Almacenar valor en el caché
  put(key, value, ttl = this.defaultTTL) {
    const now = new Date();
    const item = {
      value: value,
      expiry: now.getTime() + ttl, // Establecer el tiempo de expiración
    };
    localStorage.setItem(key, JSON.stringify(item));
  }

  // Recuperar valor del caché
  get(key) {
    const itemStr = localStorage.getItem(key);
    if (!itemStr) {
      return null; 
    }

    const item = JSON.parse(itemStr);
    const now = new Date();

    if (now.getTime() > item.expiry) {
      localStorage.removeItem(key); 
      return null; 
    }

    return item.value; 
  }
}
export default Cache;