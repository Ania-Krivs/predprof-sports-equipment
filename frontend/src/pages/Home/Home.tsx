import styles from "./Home.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { Equipment } from "../../components/Equipment/Equipment";
import { useState, useEffect } from "react";
import { getInventory } from "../../utils/requests/inventory";
import { Inventory } from "../../static/types/Inventory";

export function Home() {
  const [inventory, setInventory] = useState<Inventory[]>([]);

  useEffect(() => {
    getInventory()
      .then((inventory) => {
        setInventory(inventory);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return (
    <Layout>
      <header className={styles.header}>Инвентарь</header>
      <div className={styles.list}>
        {inventory.map((inventoryItem, index) => (
          <Equipment equipment={inventoryItem} key={index} />
        ))}
      </div>
    </Layout>
  );
}
