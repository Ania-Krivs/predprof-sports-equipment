import styles from "./Home.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { Equipment } from "../../components/Equipment/Equipment";
import { useState, useEffect } from "react";
import { getInventory } from "../../utils/requests/inventory";
import { Inventory } from "../../static/types/Inventory";
import { getInventoryRequests } from "../../utils/requests/get";
import { useCookies } from "react-cookie";
import { GetRequestResponse } from "../../static/types/Requests";
import { getUser } from "../../utils/requests/user";
import { useNavigate } from "react-router-dom";

export function Home() {
  const navigate = useNavigate();
  const [cookies] = useCookies(["SUSI_TOKEN"]);

  const [inventory, setInventory] = useState<Inventory[]>([]);
  const [requests, setRequests] = useState<GetRequestResponse[]>([]);

  useEffect(() => {
    getUser(cookies.SUSI_TOKEN).then((user) => {
      if (user.status === "USER") {
        Promise.all([getInventory(), getInventoryRequests(cookies.SUSI_TOKEN)])
          .then(([inventory, requests]) => {
            setInventory(inventory);
            setRequests(requests);
          })
          .catch((err) => {
            console.log(err);
          });
      } else if (user.status === "ADMIN") {
        navigate("/admin");
      }
    });
  }, []);

  return (
    <Layout>
      <header className={styles.header}>Инвентарь</header>
      <div className={styles.list}>
        {inventory.map((inventoryItem, index) => (
          <Equipment
            equipment={inventoryItem}
            isEditable={false}
            request={requests.find(
              (request) => request.inventory._id === inventoryItem._id
            )}
            key={index}
          />
        ))}
      </div>
    </Layout>
  );
}
