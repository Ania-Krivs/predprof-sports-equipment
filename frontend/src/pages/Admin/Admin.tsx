import styles from "./Admin.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { Inventory } from "../../static/types/Inventory";
import { Equipment } from "../../components/Equipment/Equipment";
import { getInventory } from "../../utils/requests/inventory";
import {
  getAllInventoryRequests,
  updateGetRequestStatus,
} from "../../utils/requests/get";
import { GetRequestResponse } from "../../static/types/Requests";
import { useCookies } from "react-cookie";
import { Status } from "../../static/types/Status";

export function Admin() {
  const [cookies] = useCookies(["SUSI_TOKEN"]);

  const [inventory, setInventory] = useState<Inventory[]>([]);
  const [getRequests, setGetRequests] = useState<GetRequestResponse[]>([]);

  useEffect(() => {
    getInventory()
      .then((inventory) => {
        setInventory(inventory);
      })
      .catch((err) => {
        console.log(err);
      });
    getAllInventoryRequests()
      .then((requests) => {
        setGetRequests(requests);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return (
    <Layout>
      <header className={styles.header}>Админ-панель</header>
      <Link className={styles.link} to="/admin/create">
        Создать инвентарь
      </Link>
      <div className={styles.list}>
        {inventory.map((item, index) => (
          <Equipment equipment={item} isEditable={true} key={index} />
        ))}
      </div>
      <header className={styles.header}>Заявки на получение</header>
      <div className={styles.list}>
        {getRequests.map((getRequest, index) => (
          <div className={styles.request} key={index}>
            <div className={styles.field + " " + styles.field_name}>
              {getRequest.inventory.name}
            </div>
            <div className={styles.field}>От: {getRequest.user.username}</div>
            <div className={styles.field}>
              Количество: {getRequest.quantity} шт.
            </div>
            <div className={styles.field}>
              Цель использования: {getRequest.use_purpose}
            </div>
            <div className={styles.btns}>
              <button
                className={styles.request_btn}
                onClick={() => {
                  updateGetRequestStatus(cookies.SUSI_TOKEN, {
                    application_id: getRequest._id,
                    status: Status.CANCELLED,
                  })
                    .then(() => {
                      getAllInventoryRequests()
                        .then((requests) => {
                          setGetRequests(requests);
                        })
                        .catch((err) => {
                          console.log(err);
                        });
                    })
                    .catch((err) => {
                      console.log(err);
                    });
                }}
              >
                Отклонить
              </button>
              <button
                className={styles.request_btn}
                onClick={() => {
                  updateGetRequestStatus(cookies.SUSI_TOKEN, {
                    application_id: getRequest._id,
                    status: Status.ACCEPTED,
                  })
                    .then(() => {
                      getAllInventoryRequests()
                        .then((requests) => {
                          setGetRequests(requests);
                        })
                        .catch((err) => {
                          console.log(err);
                        });
                    })
                    .catch((err) => {
                      console.log(err);
                    });
                }}
              >
                Принять
              </button>
            </div>
          </div>
        ))}
      </div>
    </Layout>
  );
}
