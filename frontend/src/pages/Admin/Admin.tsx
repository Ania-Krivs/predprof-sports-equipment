import styles from "./Admin.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { Inventory } from "../../static/types/Inventory";
import { Equipment } from "../../components/Equipment/Equipment";
import { getInventory } from "../../utils/requests/inventory";
import {
  getAllInventoryRequests,
  updateGetRequestStatus,
} from "../../utils/requests/get";
import {
  GetRequestResponse,
  RepairRequestResponse,
} from "../../static/types/Requests";
import { useCookies } from "react-cookie";
import { Status } from "../../static/types/Status";
import { getUser } from "../../utils/requests/user";
import {
  deleteRepairRequest,
  getAllRepairRequests,
} from "../../utils/requests/repair";
import { addToPlan, deleteFromPlan, getPlan } from "../../utils/requests/plan";
import { Plan } from "../../static/types/Plan";

export function Admin() {
  const navigate = useNavigate();
  const [cookies] = useCookies(["SUSI_TOKEN"]);

  const [inventory, setInventory] = useState<Inventory[]>([]);
  const [getRequests, setGetRequests] = useState<GetRequestResponse[]>([]);
  const [repairRequests, setRepairRequests] = useState<RepairRequestResponse[]>(
    []
  );
  const [plan, setPlan] = useState<Plan[]>([]);

  const [name, setName] = useState<string>("");
  const [manufacturer, setManufacturer] = useState<string>("");
  const [price, setPrice] = useState<string>("");

  function renderAdmin() {
    getInventory()
      .then((inventory) => {
        setInventory(inventory);
        setName(inventory[0].name);
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

    getAllRepairRequests(cookies.SUSI_TOKEN)
      .then((requests) => {
        setRepairRequests(requests);
      })
      .catch((err) => {
        console.log(err);
      });

    getPlan(cookies.SUSI_TOKEN)
      .then((plan) => {
        setPlan(plan);
      })
      .catch((err) => {
        console.log(err);
      });
  }

  useEffect(() => {
    getUser(cookies.SUSI_TOKEN).then((user) => {
      if (user.status === "ADMIN") {
        renderAdmin();
      } else {
        navigate("/");
      }
    });
  }, []);

  return (
    <Layout>
      <header className={styles.header}>Админ-панель</header>
      <a
        href={`${
          import.meta.env.VITE_API_URL
        }/inventory/export_table/inventory`}
        download
        target="_blank"
        className={styles.file}
      >
        Отчет по инвентарю
      </a>
      <a
        href={`${
          import.meta.env.VITE_API_URL
        }/inventory/export_table/applications`}
        download
        target="_blank"
        className={styles.file}
      >
        Отчет по заявкам
      </a>
      <a
        href={`${
          import.meta.env.VITE_API_URL
        }/inventory/export_table/inventory_repair`}
        download
        target="_blank"
        className={styles.file}
      >
        Отчет по ремонту
      </a>

      <Link className={styles.link} to="/admin/create">
        Создать инвентарь
      </Link>

      <div className={styles.list}>
        {inventory.map((item, index) => (
          <Equipment equipment={item} isEditable={true} key={index} />
        ))}
      </div>

      {getRequests.filter((request) => request.status === Status.AWAITING)
        .length > 0 ? (
        <header className={styles.header}>Заявки на получение</header>
      ) : (
        ""
      )}
      <div className={styles.list}>
        {getRequests
          .filter((request) => request.status === Status.AWAITING)
          .map((getRequest, index) => (
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
                        renderAdmin();
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

      {getRequests.filter((request) => request.status === Status.ACCEPTED)
        .length > 0 ? (
        <header className={styles.header}>В пользовании</header>
      ) : (
        ""
      )}
      <div className={styles.list}>
        {getRequests
          .filter((request) => request.status === Status.ACCEPTED)
          .map((getRequest, index) => (
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
                      status: Status.RETURNED,
                    })
                      .then(() => {
                        renderAdmin();
                      })
                      .catch((err) => {
                        console.log(err);
                      });
                  }}
                >
                  Вернул
                </button>
              </div>
            </div>
          ))}
      </div>
      {repairRequests.length > 0 ? (
        <header className={styles.header}>Заявки на ремонт</header>
      ) : (
        ""
      )}
      <div className={styles.list}>
        {repairRequests.map((repairRequest, index) => (
          <div className={styles.request} key={index}>
            <div className={styles.field + " " + styles.field_name}>
              {repairRequest.inventory.name}
            </div>
            <div className={styles.field}>
              От: {repairRequest.user.username}
            </div>
            <div className={styles.field}>
              Описание: {repairRequest.description}
            </div>
            <div className={styles.btns}>
              <button
                className={styles.request_btn}
                onClick={() => {
                  deleteRepairRequest(cookies.SUSI_TOKEN, repairRequest._id)
                    .then(() => {
                      renderAdmin();
                    })
                    .catch((err) => {
                      console.log(err);
                    });
                }}
              >
                Удалить
              </button>
            </div>
          </div>
        ))}
      </div>

      <header className={styles.header}>План закупок</header>
      <div className={styles.list}>
        {plan.map((planItem, index) => (
          <div className={styles.plan} key={index}>
            <div className={styles.plan_field}>
              Оборудование: {planItem.name}
            </div>
            <div className={styles.plan_field}>
              Производитель: {planItem.manufacturer}
            </div>
            <div className={styles.plan_field}>Цена: {planItem.price}₽</div>
            <div
              className={styles.plan_field + " " + styles.plan_field_delete}
              onClick={() => {
                deleteFromPlan(cookies.SUSI_TOKEN, planItem._id)
                  .then(() => {
                    renderAdmin();
                  })
                  .catch((err) => {
                    console.log(err);
                  });
              }}
            >
              Удалить
            </div>
          </div>
        ))}
        <div className={styles.plan}>
          <select
            className={styles.input}
            onChange={(evt) => setName(evt.target.value)}
          >
            {inventory.map((inventoryItem, index) => (
              <option value={inventoryItem.name} key={index}>
                {inventoryItem.name}
              </option>
            ))}
          </select>
          <input
            type="text"
            className={styles.input}
            placeholder="Производитель"
            onChange={(evt) => setManufacturer(evt.target.value)}
          />
          <input
            type="number"
            className={styles.input}
            placeholder="Цена (₽)"
            onChange={(evt) => setPrice(evt.target.value)}
          />
          <button
            className={styles.btn}
            onClick={() => {
              if (name && manufacturer && price && !isNaN(Number(price))) {
                addToPlan(cookies.SUSI_TOKEN, {
                  name: name,
                  manufacturer: manufacturer,
                  price: Number(price),
                })
                  .then(() => {
                    renderAdmin();
                  })
                  .catch((err) => {
                    console.log(err);
                  });
              }
            }}
          >
            Добавить
          </button>
        </div>
      </div>
    </Layout>
  );
}
